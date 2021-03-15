import time
import cv2
import os


class VideoConverter:
    def __init__(self, filename: str, scale: float, width_stretch: float, gradient: str):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        self.filename = filename
        self.scale = scale
        self.width_stretch = width_stretch
        self.gradient = list(gradient)
        self.gradient_length = len(gradient)

        self.video = cv2.VideoCapture(filename)
        self.ascii_frames = []
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.width = self.video.get(3)
        self.height = self.video.get(4)

        self.scaled_dimensions = (
            round(self.width * self.scale * self.width_stretch),
            round(self.height * self.scale),
        )

        self.line_breaks = "\n" * (os.get_terminal_size().lines - self.scaled_dimensions[1])

        # if os.name == "nt":
        #     self.clear = lambda: os.system("cls")
        # else:
        #     self.clear = lambda: os.system("clear")

    def convert(self):
        def convert_(frame):
            for row in frame:
                for b, g, r in row:
                    lumination = 0.2126 * r + 0.7152 * g + 0.0722 * b
                    yield self.gradient[int((lumination / 255) * (self.gradient_length - 1))]

                yield "\n"

        while True:
            success, frame = self.video.read()

            if not success:
                break

            frame = cv2.resize(frame, self.scaled_dimensions).tolist()
            self.ascii_frames.append("".join(convert_(frame)))

        return self

    def view(self, fps: float = None):
        if fps is None:
            spf = 1 / self.fps
        else:
            spf = 1 / fps

        try:
            for frame in self.ascii_frames:
                start = time.time()
                print(self.line_breaks + frame + "\r", end="")
                time.sleep(spf - (start - time.time()))
        except KeyboardInterrupt:
            print()
