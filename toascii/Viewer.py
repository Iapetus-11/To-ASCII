import time
import os
import cv2

class VideoViewer:
    def __init__(self, meta):
        self.__dict__ = meta

        self.current_frame = 0  # used for __iter__
        self.pretty_frames = list(map(self._pretty_frame, self.frames)) # list of prettified (finished) frames
        self.end_frame = len(self.pretty_frames)  # last frame in the list

        # determine what command to use depending on the current os
        if os.name == 'nt':
            self.clear_cmd = 'cls'
        else:
            self.clear_cmd = 'clear'

    def _pretty_frame(self, frame):  # function to basically "render" the frame
        return ''.join([f'\n{"".join(row)}' for row in frame])

    def view(self, *, fps: float=None):  # function to view all the frames in the console like a video
        if fps is None:
            spf = 1/self.fps
        else:
            spf = 1/fps

        for frame in self.pretty_frames:
            start = time.perf_counter()
            print(frame)
            diff = start - time.perf_counter()
            time.sleep((diff + abs(diff)) / 2)
            os.system(self.clear_cmd)

    def __iter__(self):  # used for iteration like in for loops
        return self

    def __next__(self):  # used for iteration like in for loops
        if self.current_frame > self.end_frame:
            raise StopIteration
        else:
            self.current_frame += 1
            return self.pretty_frames[self.current_frame - 1]
