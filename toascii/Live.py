import typing
import time
import cv2
import os

from .Constants import *


class Live:
    def __init__(self, source: int = 0, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, fps: int = 10):
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

        # determine what the clear command will be when viewing the final pretty frames
        if os.name == 'nt':
            self.clear_cmd = 'cls'
        else:
            self.clear_cmd = 'clear'

    def asciify_pixel(self, p):  # takes [r, g, b]
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(len(self.gradient)-1))/255)]

    def asciify_row(self, row):  # returns a flattened map (so a list)
        return (*map(self.asciify_pixel, row),)  # use * (all/star operator) to "flatten" the map() instead of a lazy map

    def asciify_img(self, img):  # returns a flattened map (so a list)
        return ''.join([f'\n{"".join(row)}' for row in map(self.asciify_row, img)])

    def view(self):
        spf = 1/self.fps

        try:
            while True:
                start = time.perf_counter()

                succ, img = self.video.read()

                # resize image to scaled dims in __init__
                img = cv2.resize(img, (self.scaled_width, self.scaled_height,))

                # print asciified image
                print(self.asciify_img(img))

                diff = start - time.perf_counter()
                time.sleep((diff + abs(diff)) / 2)
                os.system(self.clear_cmd)
        except KeyboardInterrupt:
            pass
