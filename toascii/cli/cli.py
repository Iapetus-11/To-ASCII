import os
import sys
from typing import Union

from .. import ConverterOptions, Image, Video, __version__, gradients
from .args import MediaType, parse_args


def main():
    print(f"To-ASCII version {__version__}\n")

    args, errors = parse_args()

    if args["help"]:
        print("Usage:")
        print("\ttoascii <media_type> <source> <converter> [--gradient <string>] [--width <int>] [--height <int>] "
              "[--xstretch <float>] [--ystretch <float>] [--saturation <float>] [--contrast <float>] [--loop]"
        )
        print("\n(Required arguments are surrounded in <>, optional arguments are surrounded in [])")
        return

    if errors:
        print("ERROR:", errors[0])
        sys.exit(1)

    if "gradient" not in args:
        args["gradient"] = gradients.LOW

    if "height" not in args:
        height = os.get_terminal_size().lines // 2
        height -= 5 if height > 10 else 0
        args["height"] = max(height, 16)

    conv_opts = ConverterOptions(
        **{k: v for k, v in args.items() if k in ConverterOptions.schema()["properties"].keys()}
    )

    cls = {MediaType.IMAGE: Image, MediaType.VIDEO: Video}[args["media_type"]]

    cls_inst: Union[Image, Video] = cls(args["source"], args["converter"](conv_opts))
    cls_inst.view()


if __name__ == "__main__":
    main()
