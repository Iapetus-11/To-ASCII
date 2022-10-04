import os
import time
from typing import Generator, Optional

import cv2

from .converters import BaseConverter
from .media_source import VIDEO_SOURCE, VideoSource


class Video:
    def __init__(
        self,
        source: VIDEO_SOURCE,
        converter: BaseConverter,
        *,
        fps: Optional[float] = None,
        loop: bool = False,
    ):
        self.source = source
        self.converter = converter
        self.options = converter.options
        self.fps = fps
        self.loop = loop

    @staticmethod
    def _validate_source(video: cv2.VideoCapture) -> None:
        if video.get(cv2.CAP_PROP_FRAME_HEIGHT) == 0:
            raise ValueError("Invalid video source provided")

    def _get_ascii_frames(self, video) -> Generator[str, None, None]:
        resize_dims = self.converter.calculate_dimensions(
            video.get(cv2.CAP_PROP_FRAME_HEIGHT),
            video.get(cv2.CAP_PROP_FRAME_HEIGHT),
        )

        while True:
            success, frame = video.read()

            # break out of loop if failed to get next frame
            if not success:
                break

            yield self.converter.asciify_image(cv2.resize(frame, resize_dims))

    def get_ascii_frames(self) -> Generator[str, None, None]:
        with VideoSource(self.source) as video:
            self._validate_source(video)

            yield from self._get_ascii_frames(video)

    @staticmethod
    def _is_live(video: cv2.VideoCapture) -> bool:
        return video.get(cv2.CAP_PROP_FRAME_COUNT) <= 0

    def view(self) -> None:
        with VideoSource(self.source) as video:
            self._validate_source(video)

            height = self.options.height or int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames = self._get_ascii_frames(video)

            # if video isn't live we should pre-gen frames
            if not self._is_live(video):
                max_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                genned_frames = []

                for i, frame in enumerate(frames, start=1):
                    genned_frames.append(frame)
                    print(f"Generating frames... ({i}/{max_frames})", end="\r")

                frames = genned_frames

            video_fps = video.get(cv2.CAP_PROP_FPS)
            seconds_per_frame = 1 / (self.fps if self.fps else video_fps)
            line_breaks = ("\n" * (os.get_terminal_size().lines - height)) + "\r"

            def _view():
                start = time.time()

                for frame in frames:
                    print(line_breaks + frame, end="\r")
                    time.sleep(seconds_per_frame - (start - time.time()))
                    start = time.time()

            _view()
            while self.loop:
                _view()
