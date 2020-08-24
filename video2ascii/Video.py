import cv2


class Video:
    def __init__(self, filename: str, *, scaled: tuple = (100, 'w'), w_stretch: float = 1, gradient: typing.Union[int, str] = 0):
        self.filename = filename
