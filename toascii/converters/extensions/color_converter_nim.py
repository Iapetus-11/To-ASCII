import pathlib
from typing import Generator
import nimporter
import numpy as np

from . import color_converter
from ..color_converter import RGB_TO_ASCII_CODE, ColorConverter

nimporter.build_nim_extensions(pathlib.Path("./toascii/converters/extensions"))

color_converter.setRgbValuesMap(list(RGB_TO_ASCII_CODE.items()))


class ColorConverterNim(ColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        yield color_converter.asciifyImage(image, list(self.options.gradient), self.options.saturation)
