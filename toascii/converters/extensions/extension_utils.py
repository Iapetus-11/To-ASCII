import pathlib

import nimporter
import numpy as np

_did_build_extensions = False


def build_extensions() -> None:
    global _did_build_extensions
    if not _did_build_extensions:
        nimporter.build_nim_extensions(pathlib.Path(__file__).parent.resolve())
        _did_build_extensions = True


def validate_image_buffer(image: np.ndarray) -> np.ndarray:
    """Return a buffer that is safe for the native converters to access."""
    if image.dtype != np.uint8:
        raise TypeError("image must use the uint8 dtype")
    if image.ndim != 3 or image.shape[2] != 3 or image.shape[0] == 0 or image.shape[1] == 0:
        raise ValueError("image must be a non-empty height x width x 3 array")

    return np.ascontiguousarray(image)
