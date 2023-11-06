from typing import Generator

import numpy as np

from ..grayscale_converter import GrayscaleConverter
from .extension_utils import build_extensions

build_extensions()

from . import grayscale_converter  # noqa


class GrayscaleConverterNim(GrayscaleConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        yield grayscale_converter.asciifyImage(image, list(self.options.gradient))
