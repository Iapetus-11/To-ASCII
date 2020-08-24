import pygame
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
            print(frame)
            time.sleep(1/fps)
            os.system('cls')

    def view(self, *, fps=None):
        fps = self.fps

        pygame.init()
        
        disp = pygame.display.set_mode((int(self.width), int(self.height),))
        pygame.display.set_caption('video2ascii')

        white = (255, 255, 255,)
        black = (0, 0, 0,)

        font = pygame.font.Font('consolas', 5)
        for frame in map(self._pretty_frame, self.frames):
            disp.fill(black)

            text = font.render(frame, white, black)

            textRect = text.get_rect()
            textRect.center = (self.width // 2, self.height // 2,)

            disp.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
