import pygame
from LITE.states import *

next_state = {
    "start_screen" : "tutorial",
    "tutorial" : "game",
    "game" : "end"
}


class Game:
    def __init__(self, screen_width=1000, screen_height=1000):
        pygame.init()

        self.running = True

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.state = "START"  # Initial state
        self.states = {
            "START": StartState(self),
            "TUTORIAL": TutorialState(self),
            "GAMEPLAY": GameplayState(self),
            "END": EndState(self)
        }

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                current_state = self.states[self.state]
                current_state.handle_events(event)

            current_state.update()
            current_state.render()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
