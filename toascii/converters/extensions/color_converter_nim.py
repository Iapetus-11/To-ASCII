from typing import Generator

import numpy as np

from ..color_converter import RGB_TO_ASCII_CODE, ColorConverter
from .extension_utils import build_extensions, validate_image_buffer

build_extensions()

from . import color_converter  # noqa

color_converter.setRgbValuesMap(list(RGB_TO_ASCII_CODE.items()))


class ColorConverterNim(ColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(validate_image_buffer(image))
        yield color_converter.asciifyImage(
            image, list(self.options.gradient), self.options.saturation
        )
