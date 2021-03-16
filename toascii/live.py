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

        self._gradient_len = len(gradient)
        self._video = None
        self._width = None
        self._height = None
        self._scaled_dims = None
        self._line_breaks = None

    def asciify(self, frame):
        for row in frame:
            for b, g, r in row:
                lumination = 0.2126 * r + 0.7152 * g + 0.0722 * b
                yield self.gradient[int((lumination / 255) * (self._gradient_len - 1))]

            yield "\n"

    def get_ascii_frame(self):
        success, frame = self._video.read()
        return success, "".join(self.asciify(cv2.resize(frame, self._scaled_dims).tolist()))

    def view(self):
        try:
            self._video = cv2.VideoCapture(self.source)
            self._width = self._video.get(4)
            self._height = self._video.get(3)

            self._scaled_dims = (
                round(self._width * self.scale * self.width_stretch),
                round(self._height * self.scale),
            )

            self._line_breaks = ("\n" * (os.get_terminal_size().lines - self._scaled_dims[1])) + "\r"

            while True:
                success, ascii_frame = self.get_ascii_frame()

                if not success:
                    break

                print(self._line_breaks + ascii_frame, end="")
        finally:
            try:
                self._video.release()
            except:
                pass

            print()

            self._width = None
            self._height = None
