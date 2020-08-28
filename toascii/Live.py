import typing
import time
import cv2
import os

from .ABC import ABC
from .Constants import *


class Live(ABC):
    def __init__(self, source: int = 0, *, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, fps: int = 10, verbose: int = False):
        self.source = source
        self.video = cv2.VideoCapture(self.source)

        self.fps = fps

        self.width = self.video.get(3)  # float, width of the video
        self.height = self.video.get(4)  # float, height of the video

        # if scale was given as a percentage (out of 100 rather than out of 1)
        if scale > 1:
            scale /= 100

        self.scale = scale  # scale which both dimensions are multiplied by
        self.w_stretch = w_stretch  # scale which the width dimension is multiplied by (to account for text which is taller than it is wide)

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

        self.gradient = tuple([c for c in self.gradient])  # turn self.gradient into a tuple
        self.gradient_len = len(self.gradient)

        # determine what the clear command will be when viewing the final pretty frames
        if os.name == 'nt':
            self.clear_cmd = 'cls'
        else:
            self.clear_cmd = 'clear'

        self.verbose = verbose

        if self.verbose:
            print(f'Dimensions: {self.width}x{self.height}')
            print(f'Scale Factor: {self.scale}')
            print(f'Scaled Dims: {self.scaled_width}x{self.scaled_height}')
            print(f'Gradient: \'{self.gradient}\'')
            print(f'FPS: {self.fps}')

    def view(self):
        spf = 1/self.fps

        try:
            while True:
                start = time.perf_counter()

                succ, img = self.video.read()

                # resize image to scaled dims in __init__ and flip it on the vertical axis
                img = cv2.flip(cv2.resize(img, (self.scaled_width, self.scaled_height,)), 1)

                diff = start - time.perf_counter()
                time.sleep((diff + abs(diff)) / 2)
                os.system(self.clear_cmd)

                # print asciified image
                print(self.asciify_img(img))
        except KeyboardInterrupt:
            pass
