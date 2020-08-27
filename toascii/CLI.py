import argparse

from .Image import Image
from .Video import Video

parser = argparse.ArgumentParser(
    prog='to-ascii',
    description='A tool which can convert videos, images, and gifs to ascii art!'
)

# cli args
parser.add_argument('-t', '--type', type=str, choices=['image', 'video'], dest='filetype', help='The type of file', action='store', required=True)
parser.add_argument('-f', '--file', type=str, dest='filename', help='The name of the file to convert', action='store', required=True)
parser.add_argument('-s', '--scale', type=float, dest='scale', help='The scale of the final dimensions', action='store')
parser.add_argument('-w', '--width-stretch', type=float, dest='width_stretch', help='Scale which only applies to the width', action='store')
parser.add_argument('-g', '--gradient', type=str, dest='gradient', help='The gradient pattern which will be used', action='store')

args = parser.parse_args()

try:  # attempt to make gradient an integer if the gradient was supposed to be an index
    gradient = int(gradient)
except Exception:
    pass

if filetype == 'video':
    c = Video(args.filename, scale=args.scale, w_stretch=args.width_stretch, gradient=args.gradient, verbose=True)
else:
    c = Image(args.filename, scale=args.scale, w_stretch=args.width_stretch, gradient=args.gradient, verbose=True)

try:
    c.convert()
    c.view()
except KeyboardInterrupt:
    print('Exiting...')
    pass
