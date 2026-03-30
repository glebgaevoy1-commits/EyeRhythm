import pygame
from LITE.states import *
from LITE.get_blink import *

next_state = {
    "start_screen" : "tutorial",
    "tutorial" : "game",
    "game" : "end"
}

class Game:
    def __init__(self):
        pygame.init()

        self.running = True

        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000

        pygame.display.set_caption("EyeRhythm 2026")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "START"  # Initial state
        self.states = {
            "START": StartState(self),
            "TUTORIAL": TutorialState(self),
            "CALIBRATION": CalibrationState(self),
            "GAMEPLAY": GameplayState(self),
            "END": EndState(self)
        }

        self.blink_detector = BlinkDetector(self)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                current_state = self.states[self.state]
                current_state.handle_events(event)


            blinked = self.blink_detector.update()
            current_state.update(blinked)
            current_state.render()

            pygame.display.flip()
            self.clock.tick(60)

        self.blink_detector.release()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
