from .base_converter import BaseConverter
from .color_converter import ColorConverter
from .extensions.unsupported_extension import unsupported_extension
from .grayscale_converter import GrayscaleConverter
from .html_color_converter import HtmlColorConverter
from .options import ConverterOptions

try:
    from .extensions.color_converter_nim import ColorConverterNim
except Exception as e:
    ColorConverterNim = unsupported_extension("color_converter_nim.ColorConverterNim", e)

try:
    from .extensions.grayscale_converter_nim import GrayscaleConverterNim
except Exception as e:
    GrayscaleConverterNim = unsupported_extension(
        "grayscale_converter_nim.GrayscaleConverterNim", e
    )

try:
    from .extensions.html_color_converter_nim import HtmlColorConverterNim
except Exception as e:
    HtmlColorConverterNim = unsupported_extension(
        "html_color_converter_nim.HtmlColorConverterNim", e
    )
