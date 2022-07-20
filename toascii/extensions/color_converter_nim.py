import pathlib
from typing import Generator, List, Tuple
import colorama
import nimporter
import numpy as np

from . import color_converter
from ..converters.color_converter import ColorConverter

nimporter.build_nim_extensions(pathlib.Path("./toascii/extensions"))


def _convert_to_list(image: np.ndarray) -> List[List[Tuple[int, int, int]]]:
    return [[(r, g, b) for b, g, r in row] for row in image]


class ColorConverterNim(ColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        result = str(color_converter.asciifyImage(_convert_to_list(image), list(self.options.gradient)))[2:-1]
        yield result
