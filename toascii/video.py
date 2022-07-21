import os
import time
from typing import Generator, Optional

import cv2

from .converters import BaseConverter, ConverterOptions
from .media_source import IMAGE_SOURCE, VideoSource


class Video:
    def __init__(
        self,
        source: IMAGE_SOURCE,
        options: ConverterOptions,
        converter: BaseConverter,
        fps: Optional[float] = None,
    ):
        self.source = source
        self.options = options
        self.converter = converter
        self.converter.options = options
        self.fps = fps

    @staticmethod
    def _validate_source(video: cv2.VideoCapture) -> None:
        if video.get(cv2.CAP_PROP_FRAME_HEIGHT) == 0:
            raise ValueError("Invalid video source provided")

    def _frames_to_ascii(self, video) -> Generator[str, None, None]:
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

    def frames_to_ascii(self) -> Generator[str, None, None]:
        with VideoSource(self.source) as video:
            self._validate_source(video)

            for frame in self._frames_to_ascii(video):
                yield frame

    def view(self) -> None:
        with VideoSource(self.source) as video:
            self._validate_source(video)

            height = self.options.height or int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames = self._frames_to_ascii(video)

            # check if video is live
            if (max_frames := int(video.get(cv2.CAP_PROP_FRAME_COUNT))) > -1:
                genned_frames = []
                for i, frame in enumerate(frames, start=1):
                    genned_frames.append(frame)
                    print(f"Generating frames... ({i}/{max_frames})", end="\r")

                frames = genned_frames

            video_fps = video.get(cv2.CAP_PROP_FPS)
            seconds_per_frame = 1 / (self.fps if self.fps else video_fps)

            line_breaks = ("\n" * (os.get_terminal_size().lines - height)) + "\r"

            start = time.time()

            for frame in frames:
                print(line_breaks + frame, end="\r")
                time.sleep(seconds_per_frame - (start - time.time()))
                start = time.time()
