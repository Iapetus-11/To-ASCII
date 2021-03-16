""""A package which can convert videos, images, gifs, and even live video to ASCII art!"""

__version__ = "4.0.0"

from .image import ImageConverter
from .video import VideoConverter
from .live import LiveVideoConverter

from . import gradients
