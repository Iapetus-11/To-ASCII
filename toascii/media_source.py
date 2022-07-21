import io
import pathlib
import tempfile
from typing import Any, Optional, Union

import cv2
import numpy as np

# type aliases
IMAGE_SOURCE = Union[str, bytes, io.IOBase]
VIDEO_SOURCE = Union[IMAGE_SOURCE, int]

# used for isinstance/subclass checks because <Py3.10 doesn't support those with generics
T_IMAGE_SOURCE = (str, bytes, io.IOBase)
T_VIDEO_SOURCE = (*T_IMAGE_SOURCE, int)

INVALID_MEDIA_SOURCE = "{source!r} is not an instance of bytes or IOBase."


def load_image(source: IMAGE_SOURCE) -> np.ndarray:
    if not isinstance(source, T_IMAGE_SOURCE):
        raise TypeError(INVALID_MEDIA_SOURCE.format(source=source))

    # attempt to load an image from a file, where src is the path
    if isinstance(source, str):
        if not pathlib.Path(source).exists():
            raise FileNotFoundError(source)

        return cv2.imread(source, cv2.IMREAD_COLOR)

    # attempt to load image from provided bytes / io
    data: bytes
    if isinstance(source, io.IOBase):
        data = source.read()
    else:
        data = source

    np_data = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_COLOR)


class VideoSource:
    def __init__(self, source: VIDEO_SOURCE):
        if not isinstance(source, T_VIDEO_SOURCE):
            raise TypeError(INVALID_MEDIA_SOURCE.format(source=source))

        self.source: Optional[VIDEO_SOURCE] = source

        self._video_cap: Optional[cv2.VideoCapture] = None
        self._temp_file: Optional[tempfile.NamedTemporaryFile] = None

    def __enter__(self) -> cv2.VideoCapture:
        if self.source is None:
            raise RuntimeError("The video source has already been closed.")

        if isinstance(self.source, (str, int)):
            self._video_cap = cv2.VideoCapture(self.source)
        else:
            data: bytes
            if isinstance(self.source, io.IOBase):
                data = self.source.read()
            else:
                data = self.source

            self._temp_file = tempfile.NamedTemporaryFile("wb")
            self._temp_file.write(data)

            self.source = None  # so gc can cleanup

            self._video_cap = cv2.VideoCapture(self._temp_file.name)

        return self._video_cap

    def __exit__(self, exc_type: type, exc_value: Exception, exc_tb: Any) -> None:
        if self._video_cap:
            self._video_cap.release()

        if self._temp_file:
            self._temp_file.close()

        if exc_value:
            raise exc_value
