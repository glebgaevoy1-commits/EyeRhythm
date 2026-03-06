import pygame

states = ["start_screen", "tutorial", "game", "end"]
next_state = {
    "start_screen" : "tutorial",
    "tutorial" : "game",
    "game" : "end"
}

class State_Base:
    def __init__(self, screen_width=1000, screen_height=1000):
        pygame.init()
        self.running = True
        self.screen_width, self.screen_height = screen_width, screen_height
        self.display = pygame.Surface((self.screen_width, self.screen_height))
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font_name = 'VCR_OSD_MONO.ttf'

        self.BLACK, self.WHITE, self.BLUE = (0, 0, 0), (255, 255, 255), (0, 0, 255)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Q - quit
                        self.running = False
                    if event.key == pygame.K_SPACE: #SPACE - next
                        self.state = next_state[self.state]
