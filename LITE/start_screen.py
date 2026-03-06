import pygame
from LITE.game import Game

class Start_Screen(Game):
    def __init__(self, screen_width=1000, screen_height=1000):
        super().__init__(screen_width, screen_height)

        self.running = True
        self.screen_width, self.screen_height = screen_width, screen_height
        self.display = pygame.Surface((self.screen_width, self.screen_height))
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font_name = 'VCR_OSD_MONO.ttf'

        # state
        self.state = "start_screen"

        self.BLACK, self.WHITE, self.BLUE = (0, 0, 0), (255, 255, 255), (0, 0, 255)

    def render(self):
        space_text = "Press SPACE to start."
        text_loc = (self.screen_width // 2, self.screen_height // 2)
        font = pygame.font.Font(self.font_name, 36)
        text_surface = font.render(space_text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = text_loc
        self.display.blit(text_surface, text_rect)
        pygame.display.update()

s = Start_Screen()
s.render()
