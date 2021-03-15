import typing
import time
import cv2
import os


class LiveVideoConverter:
    def __init__(self, source: typing.Union[str, int], scale: float, width_stretch: float, gradient: str):
        self.source = source
        self.scale = scale
        self.width_stretch = width_stretch
        self.gradient = list(gradient)
        self.gradient_length = len(gradient)

        self.video = None
        self.width = None
        self.height = None
        self.scaled_dimensions = None
        self.line_breaks = None

    def asciify(self, frame):
        for row in frame:
            for b, g, r in row:
                lumination = 0.2126 * r + 0.7152 * g + 0.0722 * b
                yield self.gradient[int((lumination / 255) * (self.gradient_length - 1))]

            yield "\n"

    def get_ascii_frame(self):
        success, frame = self.video.read()
        return success, "".join(self.asciify(cv2.resize(frame, self.scaled_dimensions).tolist()))

    def view(self):
        try:
            self.video = cv2.VideoCapture(self.source)
            self.width = self.video.get(4)
            self.height = self.video.get(3)

            self.scaled_dimensions = (
                round(self.width * self.scale * self.width_stretch),
                round(self.height * self.scale),
            )

            self.line_breaks = "\n" * (os.get_terminal_size().lines - self.scaled_dimensions[1])

            while True:
                success, ascii_frame = self.get_ascii_frame()

                if not success:
                    break

                print(self.line_breaks + ascii_frame + "\r", end="")
        finally:
            try:
                self.video.release()
            except:
                pass

            print()

            self.width = None
            self.height = None
