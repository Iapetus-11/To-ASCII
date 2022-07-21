from typing import Generator

import numpy as np

from .extension_utils import build_extensions

build_extensions()

from ..grayscale_converter import GrayscaleConverter
from . import grayscale_converter


class GrayscaleConverterNim(GrayscaleConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        yield grayscale_converter.asciifyImage(image, list(self.options.gradient))
