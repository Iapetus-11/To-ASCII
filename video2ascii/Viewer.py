import time
import os
import cv2

class Viewer:
    def __init__(self, meta):
        self.__dict__ = meta

        self.current_frame = 0
        self.pretty_frames = list(map(self._pretty_frame, self.frames))
        self.end_frame = len(self.pretty_frames)

        if os.name == 'nt':
            self.clear_cmd = 'cls'
        else:
            self.clear_cmd = 'clear'

    def _pretty_frame(self, frame):
        return ''.join([f'\n{"".join(row)}' for row in frame])

    def view(self, *, fps: float=None):
        if fps is None:
            spf = 1/self.video.get(cv2.CAP_PROP_FPS)
        else:
            spf = 1/fps

        for frame in self.pretty_frames:
            start = time.perf_counter()
            print(frame)
            diff = start - time.perf_counter()
            time.sleep(0 if diff > spf else diff)
            os.system(self.clear_cmd)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_frame > self.end_frame:
            raise StopIteration
        else:
            self.current_frame += 1
            return self.pretty_frames[self.current_frame - 1]
