import time
import os
import cv2

class Viewer:
    def __init__(self, meta):
        self.__dict__ = meta

    def _pretty_frame(self, frame):
        return ''.join([f'\n{"".join(row)}' for row in frame])

    def view(self, *, fps: float=None):
        if not fps:
            fps = self.video.get(cv2.CAP_PROP_FPS)

        for frame in list(map(self._pretty_frame, self.frames)):
            print(frame)
            time.sleep(1/fps)
            os.system('cls')
