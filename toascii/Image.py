import typing
import cv2
import os

from .ABC import *
from .Exceptions import *
from .Constants import *


class Image(ABC):
    def __init__(self, filename: str, *, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, verbose: int = False):
        if not os.path.isfile(filename):  # check for existence of file
            raise FileNotFound(filename)  # raise file not found error if it doesn't exist

        self.filename = filename
        self.image = cv2.imread(self.filename)  # load image

        self.width = self.image.shape[1]
        self.height = self.image.shape[0]

        self.ascii_image = None

        # if scale was given as a percentage (out of 100 rather than out of 1)
        if scale > 1:
            scale /= 100

        self.scale = scale
        self.w_stretch = w_stretch

        # scaled dimensions
        self.scaled_width = int(self.width*self.scale*self.w_stretch)
        self.scaled_height = int(self.height*self.scale)

        # determine what the gradient / brightness to character mapping will be
        if type(gradient) == int:
            if 0 > gradient > (len(gradients) - 1):
                raise IndexError(f'The gradient must either be a string or an integer between the value of 0 and {len(gradients)}.')
            else:
                self.gradient = gradients[gradient]
        else:
            self.gradient = gradient

        self.gradient_len = len(gradient)

        self.verbose = verbose  # whether or not to do extra logging of information

        if self.verbose:
            print(f'Dimensions: {self.width}x{self.height}')
            print(f'scale Factor: {self.scale}')
            print(f'Scaled Dims: {self.width*self.scale*self.w_stretch}x{self.height*self.scale}')
            print(f'Gradient: \'{self.gradient}\'')

    def convert(self):
        if self.verbose: print('Converting...')

        # resize image to the scale specified in __init__
        img = cv2.resize(img, (self.scaled_width, self.scaled_height,))

        self.ascii_image = self.asciify_img(img)  # asciify image

        if self.verbose: print('Done.')

        return self  # return self for fluent chaining

    def view(self):
        print(self.ascii_image)
