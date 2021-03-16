import cv2
import os

from .converter import Converter


class ImageConverter(Converter):
    """A converter class which handles converting images into ASCII."""

    def __init__(self, filename: str, scale: float, width_stretch: float, gradient: str):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        self.filename = filename
        self.scale = scale
        self.width_stretch = width_stretch
        self.gradient = list(gradient)

        self._gradient_len = len(gradient)
        self._image = cv2.imread(filename)
        self._width, self._height = reversed(self._image.shape[:2])
        self._scaled_dims = (
            round(self._width * self.scale * self.width_stretch),
            round(self._height * self.scale),
        )

        self.ascii_image = None

    def convert(self):
        image = cv2.resize(self._image, self._scaled_dims).tolist()
        self.ascii_image = "".join(self.asciify(image))

        return self

    def view(self):
        print(self.ascii_image)
