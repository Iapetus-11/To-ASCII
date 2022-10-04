from typing import Generator

import numpy as np

from .color_converter import ColorConverter


class HtmlColorConverter(ColorConverter):
    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        g_l_m = len(self.options.gradient) - 1

        last_color = None

        row: np.ndarray
        for row in image:
            for b, g, r in row:
                color = self._saturate((r, g, b), self.options.saturation)
                lum = self._luminosity(r, g, b)
                char = self.options.gradient[int((lum / 255) * g_l_m)]

                if color != last_color:
                    if last_color is not None:
                        yield "</span>"

                    last_color = color
                    yield f"""<span style="color:rgb({','.join(map(str, color))})">"""

                yield char

            yield "<br>"

        yield "</span>"

    def asciify_image(self, image: np.ndarray) -> str:
        return f'<div style="font-family:monospace;background-color:black;white-space:pre;">{"".join(self._asciify_image(image))}</div>'
