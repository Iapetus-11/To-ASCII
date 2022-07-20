from .converters import BaseConverter, ConverterOptions
from .media_source import IMAGE_SOURCE, load_image


class Image:
    def __init__(self, source: IMAGE_SOURCE, options: ConverterOptions, converter: BaseConverter):
        self.source = source
        self.options = options
        self.converter = converter
        self.converter.options = options

    def to_ascii(self) -> str:
        image = load_image(self.source)
        image = self.converter.resize_image(image)
        return self.converter.asciify_image()

    def view(self) -> None:
        print(self.to_ascii())
