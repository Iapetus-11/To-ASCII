from .converters import BaseConverter
from .media_source import IMAGE_SOURCE, load_image


class Image:
    def __init__(self, source: IMAGE_SOURCE, converter: BaseConverter):
        self.source = source
        self.converter = converter
        self.options = converter.options

    def to_ascii(self) -> str:
        image = load_image(self.source)

        if image is None:
            raise ValueError("Invalid image source provided")

        return self.converter.asciify_image(self.converter.apply_opencv_fx(image))

    def view(self) -> None:
        print(self.to_ascii())
