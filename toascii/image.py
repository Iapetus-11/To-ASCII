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
        self.gradient_length = len(gradient)

        self.image = cv2.imread(filename)
        self.ascii = None
        self.width, self.height = reversed(self.image.shape[:2])

        self.scaled_dimensions = (
            round(self.width * self.scale * self.width_stretch),
            round(self.height * self.scale),
        )

    def convert(self):
        image = cv2.resize(self.image, self.scaled_dimensions).tolist()

        def convert_():
            for row in image:
                for b, g, r in row:
                    lumination = 0.2126 * (r / 255) + 0.7152 * (g / 255) + 0.0722 * (b / 255)
                    yield self.gradient[int(lumination * self.gradient_length)]

                yield "\n"

        self.ascii = "".join(convert_())

        return self

    def view(self):
        print(self.ascii)
