import argparse


parser = argparse.ArgumentParser(
    prog='to-ascii',
    description='A tool which can convert videos, images, and gifs to ascii art!'
)

parser.add_argument('-t', '--type', type=str, choices=['image', 'video'], dest='filetype', help='The type of file', action='store', required=True)
parser.add_argument('-f', '--file', type=str, dest='filename', help='The name of the file to convert', action='store', required=True)
parser.add_argument('-s', '--scale', type=float, dest='scale', help='The scale of the final dimensions', action='store')
parser.add_argument('-w', '--width-stretch', type=float, dest='width_stretch', help='Scale which only applies to the width', action='Store')
parser.add_argument('-g', '--gradient', type=str)
