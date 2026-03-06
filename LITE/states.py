import pygame


class BaseState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.game.running = False
    def update(self):
        pass

    def render(self):
        pass

class StartState(BaseState):
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "TUTORIAL"

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((0, 0, 255))
        # Draw menu items here

class TutorialState(BaseState):
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "GAMEPLAY"

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((94, 167, 255))
        # Draw gameplay elements here

class GameplayState(BaseState):
    def handle_events(self, event):
        super().handle_events(event)

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((255, 255, 255))  # Yellow screen
        # Draw pause menu here

class EndState(BaseState):
    def handle_events(self, event):
        super().handle_events(event)

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((255, 0, 0))  # Red screen
        # Draw game over elements here
