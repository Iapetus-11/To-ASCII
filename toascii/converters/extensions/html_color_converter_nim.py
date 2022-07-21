import pathlib
from typing import Generator

import nimporter
import numpy as np

from ..html_color_converter import HtmlColorConverter
from . import html_color_converter

nimporter.build_nim_extensions(pathlib.Path("./toascii/converters/extensions"))


class HtmlColorConverterNim(HtmlColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        yield html_color_converter.asciifyImage(
            image, list(self.options.gradient), self.options.saturation
        )
