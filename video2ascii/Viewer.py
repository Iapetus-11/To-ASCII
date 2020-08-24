import time
import os
import cv2

class Viewer:
    def __init__(self, meta):
        self.__dict__ = meta

        self.current_frame = 0
        self.pretty_frames = list(map(self._pretty_frame, self.frames))
        self.end_frame = len(self.pretty_frames)

    def _pretty_frame(self, frame):
        return ''.join([f'\n{"".join(row)}' for row in frame])

    def view(self, *, fps: float=None):
        if fps is None:
            fps = self.video.get(cv2.CAP_PROP_FPS)

        for frame in self.pretty_frames:
            print(frame)
            time.sleep(1/fps)
            os.system('cls')

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_frame > self.end_frame:
            raise StopIteration
        else:
            self.current_frame += 1
            return self.pretty_frames[self.current_frame - 1]
