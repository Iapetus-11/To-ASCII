import time
import os


class Viewer:
    def __init__(self, meta):
        self.__dict__ = meta

    def _pretty_frame(self, frame):
        body = ''

        for row in frame:
            body += f'\n{"".join(row)}'

        return body

    def classic_view(self, *, fps=None):
        frames = map(self._pretty_frame, self.frames)
        fps = self.video.get(cv2.CAP_PROP_FPS)

        for frame in frames:
            print(frame)

            time.sleep(1/fps)

            os.system('cls')
