import pygame

class RythmBall():
    def __init__(self, screen, pos, color=(0, 0, 0), size_min=100, size_max=250):
        self.screen = screen
        self.pos = pos
        self.color = color
        self.size_min = size_min
        self.size_max = size_max
    def draw(self, size):
        pygame.draw.circle(self.screen, self.color, self.pos, size)
        pygame.draw.circle(self.screen, (0, 0, 255), self.pos, self.size_min)