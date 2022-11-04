import enum
import os
import time
from typing import Generator, Optional

import cv2

from .converters import BaseConverter
from .media_source import VIDEO_SOURCE, VideoSource


class FrameClearStrategy(enum.Enum):
    NONE = enum.auto()
    DOUBLE_LINE_BREAK = enum.auto()
    TERMINAL_HEIGHT_LINE_BREAKS = enum.auto()
    ANSI_ERASE_IN_LINE = enum.auto()
    ANSI_ERASE_IN_DISPLAY = enum.auto()
    ANSI_CURSOR_POS = enum.auto()


class Video:
    def __init__(
        self,
        source: VIDEO_SOURCE,
        converter: BaseConverter,
        *,
        fps: Optional[float] = None,
        loop: bool = False,
        frame_clear_strategy: FrameClearStrategy = FrameClearStrategy.ANSI_ERASE_IN_DISPLAY,
    ):
        self.source = source
        self.converter = converter
        self.options = converter.options
        self.fps = fps
        self.loop = loop
        self.frame_clear_strategy = frame_clear_strategy

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

            yield self.converter.asciify_image(
                self.converter.apply_opencv_fx(frame, resize_dims=resize_dims)
            )

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

            print_prefix = ""
            print_suffix = ""
            if self.frame_clear_strategy is FrameClearStrategy.DOUBLE_LINE_BREAK:
                print_prefix = "\n\n"
                print_suffix = "\n"
            elif self.frame_clear_strategy is FrameClearStrategy.TERMINAL_HEIGHT_LINE_BREAKS:
                print_prefix = ("\n" * (os.get_terminal_size().lines - height)) + "\r"
                print_suffix = "\r"
            elif self.frame_clear_strategy is FrameClearStrategy.ANSI_ERASE_IN_LINE:
                print_prefix = f"\033[{height}A\033[2K"
            elif self.frame_clear_strategy is FrameClearStrategy.ANSI_ERASE_IN_DISPLAY:
                print_prefix = "\033[2J"
            elif self.frame_clear_strategy is FrameClearStrategy.ANSI_CURSOR_POS:
                print_prefix = f"\033[H"

            def _view():
                start = time.time()

                for frame in frames:
                    print(print_prefix + frame, end=print_suffix)
                    time.sleep(seconds_per_frame - (start - time.time()))
                    start = time.time()

            _view()
            while self.loop:
                _view()
