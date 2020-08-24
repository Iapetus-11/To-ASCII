import cv2
import os

class FileNotFound(Exception):
    def __init__(self, file: str, msg: str = 'File \'{0}\' not found!'):
        self.file = file
        self.msg = msg.format(file)

    def __str__(self):
        return self.msg


class Video:
    def __init__(self, filename: str, *, scaled_amount: int = 100, scaled_dim: str = 'w', w_stretch: float = 1, gradient: typing.Union[int, str] = 0):
        if not os.path.isfile(filename):
            raise FileNotFound(filename)

        self.filename = filename

        self.video = cv2.VideoCapture(filename)

        if scaled_dim.lower() in ('w', 'width',):
            pass
        elif scaled_dim.lower() in ('h', 'height'):
            pass
        else:
            raise ValueError('The scaled_dim kwarg must be of the value "w", "width", "h", or "height".')

        if type(gradient) == int:
            if 0 > gradient > (len(gradients) - 1):
                raise IndexError(f'The gradient must either be a string or an integer between the value of 0 and {len(gradients)}.')
            else:
                self.gradient = gradients[gradient]
        else:
            self.gradient = gradient

    def asciify_pixel(p):  # takes [r, g, b]
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(len(self.gradient)-1))/255)]

    def asciify_frame(frame):
        return map(asciify_pixel, frame)

    def convert():
        while True:
            succ, image = self.video.read()

            if not succ:
                break

            for
