from typing import Generator

import numpy as np

from .base_converter import BaseConverter


class GrayscaleConverter(BaseConverter):
    @staticmethod
    def _luminosity(r: int, g: int, b: int) -> float:
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        g_l_m = len(self.options.gradient) - 1

        row: np.ndarray
        for row in image:
            for b, g, r in row:
                lumination = self._luminosity(r, g, b)
                yield self.options.gradient[int((lumination / 255) * g_l_m)]

            yield "\n"

    def asciify_image(self, image: np.ndarray) -> str:
        return "".join(self._asciify_image(image))
