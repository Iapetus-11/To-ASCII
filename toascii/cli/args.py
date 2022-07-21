import enum
import shlex
import sys
from typing import Any, Callable, Dict, Generic, List, TypeVar, Union

from .. import converters


def error(message: str) -> None:
    print("ERROR:", message)
    sys.exit(1)


T = TypeVar("T")


class ArgConverterException(ValueError):
    def __init__(self, message: str):
        self.message = message


class ArgDef(Generic[T]):
    __slots__ = ("name", "prefix", "converter", "optional")

    def __init__(
        self,
        name: str,
        prefix: Union[str, int],
        converter: Callable[[str], T],
        optional: bool = False,
    ):
        self.name = name
        self.prefix = prefix
        self.converter = converter
        self.optional = optional

    def convert(self, value: str) -> T:
        try:
            return self.converter(value)
        except ArgConverterException as e:
            error(f"parsing argument failed [{self.name}]: {e.message}")

    def __str__(self) -> str:
        arg_crtype = self.converter.__annotations__.get("return", str)
        arg_crtype_str = f"<{getattr(arg_crtype, '__name__', repr(arg_crtype))}>"

        if isinstance(self.prefix, int):
            return f"[{self.name} ({arg_crtype_str}, position={self.prefix})]"

        return f"[{self.name} ({self.prefix} {arg_crtype_str})]"


class MediaType(enum.Enum):
    IMAGE = enum.auto()
    VIDEO = enum.auto()


def ca_media_type(value: str) -> MediaType:
    try:
        return MediaType[value.upper()]
    except KeyError:
        raise ArgConverterException(f"invalid value: {value!r}")


def ca_source(value: str) -> Union[str, int]:
    if value.isdecimal():
        return int(value)

    return value.strip('"')


def ca_str(value: str) -> str:
    return value.strip('"')


def ca_converter(value: str) -> converters.BaseConverter:
    opts = {
        c.__name__.lower(): c
        for c in map(lambda a: getattr(converters, a), dir(converters))
        if (isinstance(c, type) and issubclass(c, converters.BaseConverter))
    }

    if (value := value.lower()) not in opts:
        raise ArgConverterException(
            f"invalid value: {value!r} (must be one of [{', '.join(map(lambda o: o.__name__.split('.')[-1], opts.values()))}])"
        )

    return opts[value]


def ca_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ArgConverterException(f"invalid value for a decimal number: {value!r}")


def ca_int(value: str) -> float:
    try:
        return int(value)
    except ValueError:
        raise ArgConverterException(f"invalid value for an integer number: {value!r}")


ARGS: Dict[Union[str, int], ArgDef] = {
    a.prefix: a
    for a in [
        ArgDef("media_type", 0, ca_media_type),
        ArgDef("source", 1, ca_source),
        ArgDef("converter", 2, ca_converter),
        ArgDef("gradient", "--gradient", ca_str, optional=True),
        ArgDef("width", "--width", ca_int, optional=True),
        ArgDef("height", "--height", ca_int, optional=True),
        ArgDef("x_stretch", "--xstretch", ca_float, optional=True),
        ArgDef("y_stretch", "--ystretch", ca_float, optional=True),
        ArgDef("saturation", "--saturation", ca_float, optional=True),
        ArgDef("contrast", "--contrast", ca_float, optional=True),
    ]
}


def get_args() -> Dict[str, Any]:
    argvj = sys.argv[1:]
    args = {}

    for prefix, arg_def in ARGS.items():
        if isinstance(prefix, int):
            if prefix > len(argvj) - 1:
                error(f"missing required positional argument {arg_def}")

            args[arg_def.name] = arg_def.convert(argvj[prefix])

    argvj = argvj[len(args) :]

    for i, arg in enumerate(argvj):
        if arg_def := ARGS.get(arg.lower()):
            if i == len(argvj) - 1 or argvj[i + 1].startswith("-"):
                error(f"missing value for argument {arg_def}")

            args[arg_def.name] = arg_def.convert(argvj[i + 1])

    for arg_def in ARGS.values():
        if arg_def.name not in args and not arg_def.optional:
            error(f"missing required argument {arg_def}")

    return args
