import pkg_resources

from . import gradients
from .converters import *
from .image import Image
from .video import FrameClearStrategy, Video

__version__ = pkg_resources.get_distribution("to-ascii").version
