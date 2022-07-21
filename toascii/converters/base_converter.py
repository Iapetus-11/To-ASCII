from abc import ABC, abstractmethod
from typing import Optional, Tuple

import cv2
import numpy as np

from .options import ConverterOptions


class BaseConverter(ABC):
    def __init__(self, options: ConverterOptions):
        self.options = options

    @abstractmethod
    def asciify_image(self, image: np.ndarray) -> str:
        """Takes a 3D numpy array containing the pixels of an image and converts it to a str"""

        raise NotImplementedError

    def calculate_dimensions(self, initial_height: int, initial_width: int) -> Tuple[int, int]:
        width = self.options.width
        height = self.options.height

        # keep ratio based off w
        if width and not height:
            height = initial_height / (initial_width / width)
        elif height and not width:
            width = initial_width / (initial_height / height)
        elif not (height or width):
            width = initial_width
            height = initial_height

        width *= self.options.x_stretch
        height *= self.options.y_stretch

        return (int(width), int(height))

    def resize_image(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, self.calculate_dimensions(*image.shape[:2]))
