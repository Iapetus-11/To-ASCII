from typing import Dict, Generator, List, Tuple, Union

import colorama
import numpy as np

from .grayscale_converter import GrayscaleConverter

T_COLOR = Union[List[int], Tuple[int, int, int]]
T_HSL_COLOR = Union[List[float], Tuple[float, float, float]]

COLOR_TRUNC = 128
COLOR_TRUNC_TO = 256 // COLOR_TRUNC

# generates all colors possible within the color space COLOR_TRUNC_TO
def _gen_colors() -> Generator[T_COLOR, None, None]:
    for r in range(0, COLOR_TRUNC_TO):
        for g in range(0, COLOR_TRUNC_TO):
            for b in range(0, COLOR_TRUNC_TO):
                yield (r, g, b)


def _dist_3d(a: T_COLOR, b: T_COLOR) -> float:
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

# all possible rgb values to color ascii codes
RGB_TO_ASCII_CODE: Dict[T_COLOR, str] = {
    a: getattr(
        colorama.Fore,
        RGB_TO_COLORAMA_NAME[min(RGB_TO_COLORAMA_NAME.keys(), key=(lambda b: _dist_3d(a, b)))],
    )
    for a in _gen_colors()
}


def _rgb2hsl(c: T_COLOR) -> T_HSL_COLOR:
    r = c[0] / 255.0
    g = c[1] / 255.0
    b = c[2] / 255.0
    c_min = min(r, min(g, b))
    c_max = max(r, max(g, b))
    delta = c_max - c_min
    h, s, l = [0.0] * 3

    if delta == 0.0:
        h = 0.0
    elif c_max == r:
        h = ((g - b) / delta) % 6.0
    elif c_max == g:
        h = ((b - r) / delta) + 2.0
    else:
        h = ((r - g) / delta) + 4.0

    h = round(h * 60.0)

    if h < 0.0:
        h += 360.0

    l = (c_max + c_min) / 2.0

    if delta == 0.0:
        s = 0.0
    else:
        s = delta / (1 - abs(2.0 * l - 1.0))

    s *= 100.0
    l *= 100.0

    return [h, s, l]


def _hsl2rgb(c: T_HSL_COLOR) -> T_COLOR:
    h = c[0]
    s = c[1] / 100.0
    l = c[2] / 100.0

    r, g, b = [0.0] * 3
    c = (1.0 - abs(2 * l - 1.0)) * s
    x = c * (1.0 - abs((h / 60.0) % 2.0 - 1.0))
    m = l - c / 2.0

    if 0 <= h and h < 60:
        r = c
        g = x
        b = 0
    elif 60 <= h and h < 120:
        r = x
        g = c
        b = 0
    elif 120 <= h and h < 180:
        r = 0
        g = c
        b = x
    elif 180 <= h and h < 240:
        r = 0
        g = x
        b = c
    elif 240 <= h and h < 300:
        r = x
        g = 0
        b = c
    elif 300 <= h and h < 360:
        r = c
        g = 0
        b = x

    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)

    return [r, g, b]


class ColorConverter(GrayscaleConverter):
    @staticmethod
    def _saturate(pixel: T_COLOR, saturation: float) -> T_COLOR:
        hsl = _rgb2hsl(pixel)

        if saturation >= 0:
            gray_factor = hsl[1] / 100.0
            var_interval = 100.0 - hsl[1]
            hsl[1] = hsl[1] + saturation * var_interval * gray_factor
        else:
            hsl[1] = hsl[1] + saturation * hsl[1]

        return _hsl2rgb(hsl)

    def _contrast(self, image: np.ndarray) -> np.ndarray:
        if self.options.contrast is not None:
            image = ((image - image.min()) / (image.max() - image.min())) * 255
            min_val = np.percentile(image, self.options.contrast * 50)
            max_val = np.percentile(image, 100 - self.options.contrast * 50)
            image = np.clip(image, min_val, max_val)
            image = ((image - min_val) / (max_val - min_val)) * 255
            image = image.astype(np.uint8)

        return image

    def _asciify_image(self, image: np.ndarray) -> Generator[str, None, None]:
        image = self._contrast(image)
        g_l_m = len(self.options.gradient) - 1

        row: np.ndarray
        for row in image:
            for b, g, r in row:
                yield RGB_TO_ASCII_CODE[
                    _trunc_color(*self._saturate((r, g, b), self.options.saturation))
                ]

                lum = self._luminosity(r, g, b)
                yield self.options.gradient[int((lum / 255) * g_l_m)]

            yield "\n"

    def asciify_image(self, image: np.ndarray) -> str:
        return "".join(self._asciify_image(image)) + colorama.Fore.RESET
