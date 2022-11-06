import os
import typing as t

import click

from toascii import ConverterOptions, FrameClearStrategy
from toascii import Image as AsciiImage
from toascii import Video as AsciiVideo
from toascii import converters, gradients

CONVERTER_TYPE_OPTIONS = {
    c.__name__.lower(): c
    for c in map(lambda a: getattr(converters, a), dir(converters))
    if (
        isinstance(c, type)
        and issubclass(c, converters.BaseConverter)
        and c is not converters.BaseConverter
    )
}

GRADIENTS = {
    "block": gradients.BLOCK,
    "low": gradients.LOW,
    "high": gradients.HIGH,
    "oxxo": gradients.OXXO,
}


def cb_source(ctx: click.Context, param: click.Parameter, value: str) -> t.Union[int, str]:
    try:
        return int(value)
    except ValueError:
        return value


def cb_converter(
    ctx: click.Context, param: click.Parameter, value: str
) -> converters.BaseConverter:
    return CONVERTER_TYPE_OPTIONS[value]


def cb_gradient(ctx: click.Context, param: click.Parameter, value: str) -> str:
    return GRADIENTS.get(value, value)


@click.command(name="toascii", no_args_is_help=True)
@click.argument("media_type", type=click.Choice(["image", "video"], case_sensitive=False))
@click.argument("source", type=click.STRING, callback=cb_source)
@click.argument(
    "converter",
    type=click.Choice(list(CONVERTER_TYPE_OPTIONS), case_sensitive=False),
    callback=cb_converter,
)
@click.option("--gradient", "-g", type=click.STRING, callback=cb_gradient, default=gradients.LOW)
@click.option("--width", "-w", type=click.IntRange(min=1))
@click.option("--height", "-h", type=click.IntRange(min=1))
@click.option(
    "--x-stretch", "--xstretch", type=click.FloatRange(min=0.0, min_open=True), default=1.0
)
@click.option(
    "--y-stretch", "--ystretch", type=click.FloatRange(min=0.0, min_open=True), default=1.0
)
@click.option("--saturation", type=click.FloatRange(min=-1.0, max=1.0), default=0.5)
@click.option("--contrast", type=click.FloatRange(min=0.0, max=1.0))
@click.option("--blur", type=click.IntRange(min=2))
@click.option("--loop", is_flag=True)
def toascii_command(**kwargs):
    if not kwargs.get("height"):
        kwargs["height"] = max(min(os.get_terminal_size().lines - 1, 32), 4)

    media_type: t.Literal["image", "video"] = kwargs.pop("media_type")

    if media_type == "video":
        kwargs["frame_clear_strategy"] = FrameClearStrategy.ANSI_ERASE_IN_LINE
    else:
        del kwargs["loop"]

    converter_options = ConverterOptions(
        **{
            k: kwargs.pop(k)
            for k in list(kwargs)
            if k in ConverterOptions.schema()["properties"].keys()
        }
    )

    kwargs["converter"] = kwargs["converter"](converter_options)

    cls = {"image": AsciiImage, "video": AsciiVideo}[media_type]
    cls_instance: t.Union[AsciiImage, AsciiVideo] = cls(**kwargs)

    cls_instance.view()
