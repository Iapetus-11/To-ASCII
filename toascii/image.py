import cv2
import os


class ImageAsciifier:
    def __init__(self, filename: str, output_dimensions: tuple[int, int], gradient: str):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        self.filename = filename
        self.output_dimensions = output_dimensions
        self.gradient = list(gradient)
        self.gradient_length = len(gradient)

        self.image = cv2.imread(filename)
        self.width, self.height = reversed(self.image.shape)

        self.s_width = round(self.width * self.scale * self.width_stretch)
        self.s_height = round(self.height * self.scale)

    def convert(self):
        image = cv2.resize(self.image, self.output_dimensions).tolist()

        def convert_():
            for row in image:
                for b, g, r in image:
                    lumination = 0.2126 * (r / 255) + 0.7152 * (g / 255) + 0.0722 * (b / 255)
                    yield self.gradient[int(lumination * self.gradient_length)]

                yield "\n"

        return "".join(convert_())

    def view(self):
        print(self.ascii_image)
