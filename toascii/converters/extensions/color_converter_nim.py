from typing import Generator

import numpy as np

from .extension_utils import build_extensions

build_extensions()

from ..color_converter import RGB_TO_ASCII_CODE, ColorConverter
from . import color_converter

color_converter.setRgbValuesMap(list(RGB_TO_ASCII_CODE.items()))


class ColorConverterNim(ColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        yield color_converter.asciifyImage(
            image, list(self.options.gradient), self.options.saturation
        )
