import sys
import os

from .image import ImageConverter
from .video import VideoConverter
from .live import LiveVideoConverter

from . import gradients

INVALID_ARGS = """Invalid arguments inputted. See below for proper usage:

asciify <type> <source> <scale> [width stretch] [gradient] [loop]

Arguments:
type            The type of content, either IMAGE, VIDEO, or LIVE.
source          The source, either a file path or video device.
scale           Used to scale down the image to fit in your console, recommended value is 0.1.
width stretch   Used to account for console characters being taller than they are wide, default value is 2.0.
gradient        The gradient used, one of BLOCK, HIGH, LOW, or a custom gradient as a string.
loop            If "loop" is the 5th argument, the displayed ASCII video will loop forever.

Required arguments are surrounded in <>, optional arguments are surrounded in [].
"""


def main():
    args = sys.argv[1:]
    # source, scale, width_stretch, gradient

    if len(args) not in (3, 4, 5, 6):
        print(INVALID_ARGS)
        exit(1)

    type_ = args[0].lower()

    if type_ not in ("image", "video", "live"):
        print(INVALID_ARGS)
        exit(1)

    source = args[1]

    try:
        source = int(source)
    except ValueError:
        pass

    if isinstance(source, str):
        if not os.path.isfile(source):
            print(f"File {source} not found.")
            exit(1)

    try:
        scale = float(args[2])
    except ValueError:
        print(INVALID_ARGS)
        exit(1)

    try:
        width_stretch = float(args[3])
    except IndexError:
        width_stretch = 2
    except ValueError:
        print(INVALID_ARGS)
        exit(1)

    try:
        gradient = args[4]
    except IndexError:
        gradient = gradients.BLOCK

    if gradient.lower() == "block":
        gradient = gradients.BLOCK
    elif gradient.lower() == "high":
        gradient = gradients.HIGH
    elif gradient.lower() == "low":
        gradient = gradients.LOW

    try:
        if args[5].lower() == "loop":
            loop = True
        else:
            loop = False
    except IndexError:
        loop = False

    if type_.lower() == "image":
        ImageConverter(source, scale, width_stretch, gradient).convert().view()
    elif type_.lower() == "video":
        VideoConverter(source, scale, width_stretch, gradient, loop).convert().view()
    elif type_.lower() == "live":
        LiveVideoConverter(source, scale, width_stretch, gradient).view()


if __name__ == "__main__":
    main()
