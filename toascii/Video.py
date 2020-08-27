import typing
import time
import cv2
import os

from .ABC import ABC
from .Exceptions import *
from .Constants import *


class Video(ABC):
    def __init__(self, filename: str, *, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, verbose: int = False):
        if not os.path.isfile(filename):  # check to make sure file actually exists
            raise FileNotFound(filename)  # FileNotFound is from .Exceptions

        self.filename = filename
        self.video = cv2.VideoCapture(filename)

        # self.frames is a frames[frame[row[char, char,..], row[],..], frame[],..]
        self.frames = []  # converted frames (will be populated when convert() is called)

        self.fps = self.video.get(cv2.CAP_PROP_FPS)  # fps of the origin video

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

        self.gradient_len = len(self.gradient)

        self.verbose = verbose  # whether or not to do extra logging of information

        # for __iter__ to allow this to be used in a for loop to iterate through the frames
        self.current_frame = 0
        self.end_frame = None

        # determine what the clear command will be when viewing the final asciified frames
        if os.name == 'nt':
            self.clear_cmd = 'cls'
        else:
            self.clear_cmd = 'clear'

        if self.verbose:
            print(f'Dimensions: {self.width}x{self.height}')
            print(f'scale Factor: {self.scale}')
            print(f'Scaled Dims: {self.scaled_width}x{self.scaled_height}')
            print(f'Gradient: \'{self.gradient}\'')

    def convert(self):  # function which is called to populate the list of converted frames (self.frames)
        if self.verbose: print('Converting...')

        while True:
            succ, img = self.video.read()  # read frame from video

            if not succ: break  # if failed when reading

            # resize image to the scale specified in __init__
            img = cv2.resize(img, (self.scaled_width, self.scaled_height,))

            self.frames.append(self.asciify_img(img))  # add the asciified image to the list of converted frames

        self.end_frame = len(self.frames)

        if self.verbose: print('Done.')

        return self  # returns self for fluent chaining

    def view(self, *, fps: float=None):  # function to view all the frames in the console like a video
        if fps is None:
            spf = 1/self.fps
        else:
            spf = 1/fps

        try:
            for frame in self.frames:
                start = time.perf_counter()
                print(frame)
                diff = start - time.perf_counter()
                time.sleep((diff + abs(diff)) / 2)
                os.system(self.clear_cmd)
        except KeyboardInterrupt:
            pass

    def __iter__(self):  # allow iteration over the frames (like in a for loop)
        return self

    def __next__(self):  # allow iteration over the frames (like in a for loop)
        if self.current_frame > self.end_frame:
            raise StopIteration

        self.current_frame += 1
        return self.frames[self.current_frame - 1]
