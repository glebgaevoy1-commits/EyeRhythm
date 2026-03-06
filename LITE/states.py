import pygame

class BaseState:
    def __init__(self, game):
        self.game = game
        self.font_path = "VCR_OSD_MONO.ttf"
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.game.running = False
    def update(self):
        pass

    def render(self):
        pass

    def draw_text(self, text, x, y, font_size=30, color=(255, 255, 255)):
        """Draws text on the screen using a specified font size."""
        font = pygame.font.Font(self.font_path, font_size)  # Load the font with the specified size
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.game.screen.blit(text_surface, text_rect)

    def draw_image(self, image_path, x, y, width=None, height=None):
        """Draws an image on the screen."""
        # Load image
        image = pygame.image.load(image_path)

        # Resize if width and height are provided
        if width and height:
            image = pygame.transform.scale(image, (width, height))

        # Get the rect for positioning
        image_rect = image.get_rect(center=(x, y))
        self.game.screen.blit(image, image_rect)



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
        title = "EyeRHYTHM"
        self.draw_text(title, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 4, 100)
        self.draw_image("eye_graphic.png", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2)

        subtitle = "press SPACE to continue..."
        self.draw_text(subtitle, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 4 * 3, 50)

        cpyright = "© 2026 Gleb Gaevoy"
        self.draw_text(cpyright, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 5 * 4, 20)



class TutorialState(BaseState):
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "CALIBRATION"

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((94, 167, 255))
        # Draw gameplay elements here
        title = "HOW TO PLAY???"
        self.draw_text(title, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 8, 100)
        self.draw_image("tutorial.png", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2)
        subtitle = "press SPACE to continue.."
        self.draw_text(subtitle, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 8 * 7, 50)


class CalibrationState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.blink_cnt = 0

    def handle_events(self, event):
        super().handle_events(event)
        if self.blink_cnt == 10:
            self.game.state = "GAMEPLAY"

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((40, 130, 255))

        title = "CALIBRATION"
        self.draw_text(title, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 8, 100)

        subtitle = f"look into the camera and blink 10 times"

        self.draw_text(subtitle, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 3, 25)

        self.draw_text(str(self.blink_cnt), self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 3 * 2, 150, color=(255, 0, 0))

class GameplayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.hits = 0
        self.misses = 0
        self.total_blinks = 0

        self.win_amm = 10
        self.lose_amm = 3

        self.misses_in_a_row = 0

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

