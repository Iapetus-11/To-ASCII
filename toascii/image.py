import cv2
import os


class ImageConverter:
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

    def asciify(self, image):
        for row in image:
            for b, g, r in row:
                lumination = 0.2126 * r + 0.7152 * g + 0.0722 * b
                yield self.gradient[int((lumination / 255) * (self._gradient_len - 1))]

            yield "\n"

    def convert(self):
        image = cv2.resize(self._image, self._scaled_dims).tolist()
        self.ascii_image = "".join(self.asciify(image))

        return self

    def view(self):
        print(self.ascii_image)
