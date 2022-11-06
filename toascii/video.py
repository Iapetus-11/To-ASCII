import enum
import os
import time
from typing import Generator, Optional, Tuple, Union

from .converters import BaseConverter
from .media_source import VIDEO_SOURCE, AbstractVideoSource, OpenCVVideoSource


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
        source: Union[VIDEO_SOURCE, AbstractVideoSource],
        converter: BaseConverter,
        *,
        fps: Optional[float] = None,
        loop: bool = False,
        frame_clear_strategy: FrameClearStrategy = FrameClearStrategy.ANSI_ERASE_IN_DISPLAY,
    ):
        self.source = (
            source if isinstance(source, AbstractVideoSource) else OpenCVVideoSource(source)
        )
        self.converter = converter
        self.options = converter.options
        self.fps = fps
        self.loop = loop
        self.frame_clear_strategy = frame_clear_strategy

    def _get_ascii_frames(self, video: AbstractVideoSource) -> Generator[str, None, None]:
        resize_dims = self.converter.calculate_dimensions(video.width, video.height)

        for frame in video:
            yield self.converter.asciify_image(
                self.converter.apply_opencv_fx(frame, resize_dims=resize_dims)
            )

    def get_ascii_frames(self) -> Generator[str, None, None]:
        with self.source as video:
            video.ensure_valid()
            yield from self._get_ascii_frames(video)

    def _get_print_affixes(self, video: AbstractVideoSource) -> Tuple[str, str]:
        print_prefix = ""
        print_suffix = ""

        if self.frame_clear_strategy is FrameClearStrategy.DOUBLE_LINE_BREAK:
            print_prefix = "\n\n"
            print_suffix = "\n"
        elif self.frame_clear_strategy is FrameClearStrategy.TERMINAL_HEIGHT_LINE_BREAKS:
            print_prefix = (
                "\n" * (os.get_terminal_size().lines - (self.options.height or video.height))
            ) + "\r"
            print_suffix = "\r"
        elif self.frame_clear_strategy is FrameClearStrategy.ANSI_ERASE_IN_LINE:
            print_prefix = f"\033[{video.height}A\033[2K"
        elif self.frame_clear_strategy is FrameClearStrategy.ANSI_ERASE_IN_DISPLAY:
            print_prefix = "\033[2J"
        elif self.frame_clear_strategy is FrameClearStrategy.ANSI_CURSOR_POS:
            print_prefix = f"\033[H"

        return print_prefix, print_suffix

    def view(self) -> None:
        with self.source as video:
            video.ensure_valid()

            frames = self._get_ascii_frames(video)

            # if video isn't live we should pre-gen frames for optimal viewing
            if not video.is_live:
                genned_frames = []

                for i, frame in enumerate(frames, start=1):
                    genned_frames.append(frame)
                    print(f"Generating frames... ({i}/{video.frame_count})", end="\r")

                frames = genned_frames

            seconds_per_frame = 1 / (self.fps if self.fps else video.fps)

            print_prefix, print_suffix = self._get_print_affixes(video)

            def _view():
                start = time.time()

                for frame in frames:
                    print(print_prefix + frame, end=print_suffix)
                    time.sleep(seconds_per_frame - (start - time.time()))
                    start = time.time()

            _view()
            while self.loop:
                _view()
