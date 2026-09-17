from typing import Generator

import numpy as np

from ..grayscale_converter import GrayscaleConverter
from .extension_utils import build_extensions, validate_image_buffer

build_extensions()

from . import grayscale_converter  # noqa


class GrayscaleConverterNim(GrayscaleConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = validate_image_buffer(image)
        yield grayscale_converter.asciifyImage(image, list(self.options.gradient))
