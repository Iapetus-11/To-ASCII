import cv2
import os
import typing

from Viewer import Viewer

class FileNotFound(Exception):
    def __init__(self, file: str, msg: str = 'File \'{0}\' not found!'):
        self.file = file
        self.msg = msg.format(file)

    def __str__(self):
        return self.msg

gradients = [
    ' `~+=*\\!0G@'
]


class Video:
    def __init__(self, filename: str, *, resize_amount: float = 1, w_stretch: float = 1, gradient: typing.Union[int, str] = 0):
        if not os.path.isfile(filename):
            raise FileNotFound(filename)

        self.filename = filename

        self.video = cv2.VideoCapture(filename)
        self.frames = []

        if resize_amount > 1:
            resize_amount /= 100

        self.resize_amount = resize_amount

        if type(gradient) == int:
            if 0 > gradient > (len(gradients) - 1):
                raise IndexError(f'The gradient must either be a string or an integer between the value of 0 and {len(gradients)}.')
            else:
                self.gradient = gradients[gradient]
        else:
            self.gradient = gradient

    def asciify_pixel(self, p):  # takes [r, g, b]
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(len(self.gradient)-1))/255)]

    def convert(self):
        while True:
            succ, img = self.video.read()

            img = cv2.resize(self.video, (int(img.shape[1]*self.resize_amount), int(img.video.shape[0]*self.resize_amount),))

            if not succ:
                break

            self.frames.append([map(asciify_pixel, row) for row in img])

        return Viewer(self.__dict__)
