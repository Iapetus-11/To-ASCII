from .extensions.unsupported_extension import UnsupportedExtension
from .base_converter import BaseConverter
from .grayscale_converter import GrayscaleConverter
from .color_converter import ColorConverter
from .options import ConverterOptions

try:
    from .extensions.color_converter_nim import ColorConverterNim
except Exception as e:
    ColorConverterNim = UnsupportedExtension("color_converter_nim.ColorConverterNim", e)
