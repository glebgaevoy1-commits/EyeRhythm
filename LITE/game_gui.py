import pygame

class Button:
    def __init__(self, screen, center_pos, dimensions, color="red", text="", text_size=50): #add subtitle to button
        self.screen = screen
        self.x, self.y = center_pos
        self.width, self.height = dimensions
        self.color = color

        self.text = text
        self.text_size = text_size

        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        if self.text:
            font = pygame.font.SysFont('VCR_OSD_MONO.ttf', self.text_size)
            text_surf = font.render(self.text, False,(0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.screen.blit(text_surf, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class RythmBall:
    def __init__(self, screen, pos, color=(0, 0, 0), size_min=100, size_max=250):
        self.screen = screen
        self.pos = pos
        self.color = color
        self.size_min = size_min
        self.size_max = size_max
    def draw(self, size):
        pygame.draw.circle(self.screen, self.color, self.pos, size)
        pygame.draw.circle(self.screen, (0, 0, 255), self.pos, self.size_min)