from typing import Generator
import nimporter
import numpy as np
import pathlib

from ..grayscale_converter import GrayscaleConverter
from . import grayscale_converter

nimporter.build_nim_extensions(pathlib.Path("./toascii/converters/extensions"))

class GrayscaleConverterNim(GrayscaleConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        yield grayscale_converter.asciifyImage(image, list(self.options.gradient))
