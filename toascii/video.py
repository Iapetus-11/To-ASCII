import os
import time
from typing import Generator, Optional

import cv2
from .media_source import IMAGE_SOURCE, VideoSource
from .converters import ConverterOptions, BaseConverter


class Video:
    def __init__(self, source: IMAGE_SOURCE, options: ConverterOptions, converter: BaseConverter, fps: Optional[float] = None):
        self.source = source
        self.options = options
        self.converter = converter
        self.converter.options = options
        self.fps = fps

    def _frames_to_ascii(self, video) -> Generator[str, None, None]:
        resize_dims = self.converter.calculate_dimensions(
            video.get(cv2.CAP_PROP_FRAME_WIDTH),
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
            for frame in self._frames_to_ascii(video):
                yield frame

    def view(self) -> None:
        with VideoSource(self.source) as video:
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

            for frame in frames:
                start = time.time()
                print(line_breaks + frame, end="\r")
                time.sleep(seconds_per_frame - (start - time.time()))
                # os.system("cls")
