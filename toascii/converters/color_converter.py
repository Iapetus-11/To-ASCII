from typing import Generator, Tuple
import numpy as np
import colorama

from .grayscale_converter import GrayscaleConverter

COLOR_TRUNC = 128
COLOR_TRUNC_TO = 256 // COLOR_TRUNC

# generates all colors possible within the color space COLOR_TRUNC_TO
def _gen_colors() -> Generator[Tuple[int, int, int], None, None]:
    for r in range(0, COLOR_TRUNC_TO):
        for g in range(0, COLOR_TRUNC_TO):
            for b in range(0, COLOR_TRUNC_TO):
                yield (r, g, b)


def _dist_3d(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
    return abs((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2)


def _trunc_color(r: int, g: int, b: int) -> Tuple[int, int, int]:
    return (r // COLOR_TRUNC, g // COLOR_TRUNC, b // COLOR_TRUNC)


RGB_TO_COLORAMA_NAME = {
    _trunc_color(*k): v
    for k, v in {
        (196, 29, 17): "RED",
        (0, 193, 32): "GREEN",
        (199, 195, 38): "YELLOW",
        (10, 47, 196): "BLUE",
        (200, 57, 197): "MAGENTA",
        (1, 197, 198): "CYAN",
        (199, 199, 199): "WHITE",
        (104, 104, 104): "LIGHTBLACK_EX",
        (255, 110, 103): "LIGHTRED_EX",
        (96, 249, 102): "LIGHTGREEN_EX",
        (255, 252, 96): "LIGHTYELLOW_EX",
        (100, 111, 253): "LIGHTBLUE_EX",
        (255, 119, 255): "LIGHTMAGENTA_EX",
        (96, 253, 255): "LIGHTCYAN_EX",
        (255, 254, 245): "LIGHTWHITE_EX",
    }.items()
}

# all possible rgb values to colorama
ALL_RGB_TO_COLORAMA_NAME = {
    a: RGB_TO_COLORAMA_NAME[min(RGB_TO_COLORAMA_NAME.keys(), key=(lambda b: _dist_3d(a, b)))] for a in _gen_colors()
}


class ColorConverter(GrayscaleConverter):
    def _color_aprox(self, r: int, g: int, b: int) -> str:
        return getattr(colorama.Fore, ALL_RGB_TO_COLORAMA_NAME[_trunc_color(r, g, b)])

    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        g_l_m = len(self.options.gradient) - 1

        row: np.ndarray
        for row in image:
            for b, g, r in row:
                yield self._color_aprox(r, g, b)

                lum = self._luminosity(r, g, b)
                yield self.options.gradient[int((lum / 255) * g_l_m)]

            yield "\n"

        yield colorama.Fore.RESET

    def asciify_image(self, image: np.ndarray) -> str:
        return "".join(self._asciify_image(image))
