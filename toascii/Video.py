import typing
import cv2
import os

from .Exceptions import *
from .Constants import *


class Video:
    def __init__(self, filename: str, *, scale: float = 1, w_stretch: float = 2, gradient: typing.Union[int, str] = 0, verbose: int = False):
        if not os.path.isfile(filename):  # check to make sure file actually exists
            raise FileNotFound(filename)  # FileNotFound is from .Exceptions

        self.filename = filename
        self.video = cv2.VideoCapture(filename)

        # self.frames is a frames[frame[row[char, char,..], row[],..], frame[],..]
        self.frames = []  # converted frames (will be populated when convert() is called)
        # self.pretty_frames is  frames[text, text, text,..]
        self.pretty_frames = None  # finished frames, "rendered" frames from self.frames

        self.fps = self.video.get(cv2.CAP_PROP_FPS)  # fps of the origin video

        self.width = self.video.get(3)  # float, width of the video
        self.height = self.video.get(4)  # float, height of the video

        # if scale was given as a percentage (out of 100 rather than out of 1)
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

        self.verbose = verbose  # whether or not to do extra logging of information

        # for __iter__ to allow this to be used in a for loop to iterate through the frames
        self.current_frame = 0
        self.end_frame = len(self.pretty_frames)

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

    def prettify_frame(self, frame):  # "render" the frame so it can be print()ed later
        return ''.join([f'\n{"".join(row)}' for row in frame])

    def prettify_frames(self):  # return a flattened map of prettified frames
        self.pretty_frames = (*map(self.pretty_frame, self.frames),)

    def convert(self):  # function which is called to populate the list of converted frames (self.frames)
        if self.verbose: print('Converting...')

        while True:
            succ, img = self.video.read()  # read frame from video

            if not succ: break  # if failed when reading

            # resize image to scales specified in __init__
            img = cv2.resize(img, (int(img.shape[1]*self.scale*self.w_stretch), int(img.shape[0]*self.scale),))

            self.frames.append(self.asciify_img(img))  # add the asciified image to the list of converted frames

        if self.verbose: print('Prettifying frames...')
        self.prettify_frames()

        if self.verbose: print('Done converting.')

        return self  # returns self for fluent chaining

    def __iter__(self):  # allow iteration over the frames (like in a for loop)
        return self

    def __next__(self):  # allow iteration over the frames (like in a for loop)
        if self.current_frame > self.end_frame:
            raise StopIteration

        self.current_frame += 1
        return self.pretty_frames[self.current_frame - 1]
