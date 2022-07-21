from typing import Generator

import numpy as np

from .extension_utils import build_extensions

build_extensions()

from ..html_color_converter import HtmlColorConverter
from . import html_color_converter


class HtmlColorConverterNim(HtmlColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        yield html_color_converter.asciifyImage(
            image, list(self.options.gradient), self.options.saturation
        )
