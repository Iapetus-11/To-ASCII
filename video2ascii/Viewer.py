import time
import os
import cv2


class Viewer:
    def __init__(self, meta):
        self.__dict__ = meta

    def _pretty_frame(self, frame):
        body = ''

        for row in frame:
            body += f'\n{"".join(row)}'

        return body

    def classic_view(self, *, fps=None):
        fps = self.video.get(cv2.CAP_PROP_FPS)

        for frame in map(self._pretty_frame, self.frames):
            print('\n'*50)
            print(frame)
            time.sleep(1/fps)
