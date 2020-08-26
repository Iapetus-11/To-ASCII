import typing
import cv2
import os

from .Exceptions import *
from .Constants import *


class Image:
    def __init__(self, filename: str, *, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, verbose: int = False):
        if not os.path.isfile(filename):  # check for existence of file
            raise FileNotFound(filename)  # raise file not found error if it doesn't exist

        self.filename = filename
        self.image = cv2.imread(self.filename)  # load image

        self.width = self.image[1]
        self.height = self.image[0]

        # if scale was given as a percentage (out of 100 rather than out of 1)
        if scale > 1:
            scale /= 100

        self.scale = scale
        self.w_stretch = w_stretch

        # determine what the gradient / brightness to character mapping will be
        if type(gradient) == int:
            if 0 > gradient > (len(gradients) - 1):
                raise IndexError(f'The gradient must either be a string or an integer between the value of 0 and {len(gradients)}.')
            else:
                self.gradient = gradients[gradient]
        else:
            self.gradient = gradient

        self.verbose = verbose  # whether or not to do extra logging of information

    if self.verbose:
        print(f'Dimensions: {self.width}x{self.height}')
        print(f'scale Factor: {self.scale}')
        print(f'Scaled Dims: {self.width*self.scale*self.w_stretch}x{self.height*self.scale}')
        print(f'Gradient: \'{self.gradient}\'')


    def asciify_pixel(self, p):  # takes [r, g, b]
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(len(self.gradient)-1))/255)]

    def asciify_row(self, row):  # returns a flattened map (so a list)
        return (*map(self.asciify_pixel, row),)  # use * (all/star operator) to "flatten" the map() instead of a lazy map

    def asciify_img(self, img):  # returns a flattened map (so a list)
        return (*map(self.asciify_row, img),)

    def prettify(self, img):  # "render" the image in ascii so it can be print()ed later
        return ''.join([f'\n{"".join(row)}' for row in img])
