import multiprocessing as mp
import typing
import cv2
import os

from .Exceptions import *
from .Constants import *
from .Viewer import Viewer


class Video:
    def __init__(self, filename: str, *, scale: float = 1, w_stretch: float = 1, gradient: typing.Union[int, str] = 0, max_workers: int = 60, verbose=False):
        if not os.path.isfile(filename):
            raise FileNotFound(filename)

        self.filename = filename

        self.video = cv2.VideoCapture(filename)
        self.frames = []  # converted frames (will be populated when convert() is called)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)  # fps of the origin video

        self.width = self.video.get(3)  # float, width of the video
        self.height = self.video.get(4)  # float, height of the video

        # if scale was given as a percentage
        if scale > 1:
            scale /= 100

        self.scale = scale  # scale which both dimensions are multiplied by
        self.w_stretch = w_stretch  # scale which the width dimension is multiplied by (to account for text which is taller than it is wide)

        # determine what the gradient / brightness to character mapping will be
        if type(gradient) == int:
            if 0 > gradient > (len(gradients) - 1):
                raise IndexError(f'The gradient must either be a string or an integer between the value of 0 and {len(gradients)}.')
            else:
                self.gradient = gradients[gradient]
        else:
            self.gradient = gradient

        self.max_workers = max_workers  # used for multiprocessing

        self.verbose = verbose  # whether or not to do extra logging of information

        if self.verbose:
            print(f'Dimensions: {self.width}x{self.height}')
            print(f'scale Factor: {self.scale}')
            print(f'Scaled Dims: {self.width*self.scale*self.w_stretch}x{self.height*self.scale}')
            print(f'Gradient: \'{self.gradient}\'')

    def asciify_pixel(self, p):  # takes [r, g, b]
        if type(p) == tuple: print(p)
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(len(self.gradient)-1))/255)]

    def asciify_row(self, row):  # returns a flattened map (so a list)
        return (*map(self.asciify_pixel, row),)

    def asciify_img(self, img):  # returns a flattened map (so a list)
        return (*map(self.asciify_row, img),)

    def convert(self):  # function which is called to populate the list of converted frames
        if self.verbose: print('Converting...')

        while True:
            succ, img = self.video.read()  # read frame from video

            if not succ: break  # if failed when reading

            # resize image to scales specified in __init__
            img = cv2.resize(img, (int(img.shape[1]*self.scale*self.w_stretch), int(img.shape[0]*self.scale),))

            self.frames.append(self.asciify_img(img))  # add the asciified image to the list of converted frames

        if self.verbose: print('Done converting.')
        return Viewer(self.__dict__)  # create a new Viewer object with all the instance variables of this object
