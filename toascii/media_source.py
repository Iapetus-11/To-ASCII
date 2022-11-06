import abc
import io
import pathlib
import tempfile
from typing import Any, Optional, Type, Union

import cv2
import numpy
import numpy as np
import typing_extensions

# type aliases
IMAGE_SOURCE = Union[str, bytes, io.IOBase]
VIDEO_SOURCE = Union[IMAGE_SOURCE, int]

# used for isinstance/subclass checks because <Py3.10 doesn't support those with generics
T_IMAGE_SOURCE = (str, bytes, io.IOBase)
T_VIDEO_SOURCE = (*T_IMAGE_SOURCE, int)


def load_image(source: IMAGE_SOURCE) -> np.ndarray:
    if not isinstance(source, T_IMAGE_SOURCE):
        raise TypeError(f"{source!r} is not an instance of bytes or IOBase.")

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


class AbstractVideoSource(abc.ABC):
    def ensure_valid(self) -> None:
        if self.fps < 1 or self.height < 1 or self.width < 1:
            raise Exception("Invalid video source provided")

    @property
    @abc.abstractmethod
    def is_live(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def fps(self) -> float:
        ...

    @property
    @abc.abstractmethod
    def width(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def height(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def frame_count(self) -> int:
        ...

    def __iter__(self) -> typing_extensions.Self:
        return self

    @abc.abstractmethod
    def __next__(self) -> numpy.ndarray:
        ...

    @abc.abstractmethod
    def __enter__(self) -> typing_extensions.Self:
        ...

    @abc.abstractmethod
    def __exit__(self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: Any) -> None:
        ...


class OpenCVVideoSource(AbstractVideoSource):
    def __init__(self, source: VIDEO_SOURCE):
        if not isinstance(source, T_VIDEO_SOURCE):
            raise TypeError(f"{source!r} is not an instance of int, bytes, or IOBase.")

        self.source: Optional[VIDEO_SOURCE] = source

        self._video_cap: Optional[cv2.VideoCapture] = None
        self._temp_file: Optional[tempfile.NamedTemporaryFile] = None

    @property
    def video_cap(self) -> cv2.VideoCapture:
        if self._video_cap is None:
            raise Exception("VideoCapture hasn't been initialized yet")

        return self._video_cap

    @property
    def is_live(self) -> bool:
        return self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT) <= 0

    @property
    def fps(self) -> float:
        return self.video_cap.get(cv2.CAP_PROP_FPS)

    @property
    def width(self) -> int:
        return int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        return int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame_count(self) -> int:
        return int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __next__(self) -> numpy.ndarray:
        success, frame = self._video_cap.read()

        if not success:
            raise StopIteration

        return frame

    def __enter__(self) -> typing_extensions.Self:
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

        return self

    def __exit__(self, exc_type: type, exc_value: Exception, exc_tb: Any) -> None:
        if self._video_cap:
            self._video_cap.release()

        if self._temp_file:
            self._temp_file.close()
