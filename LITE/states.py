import pygame
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from LITE.configs import precision_window

from game_gui import Button, RythmBall

class BaseState:
    def __init__(self, game):
        self.game = game
        self.font_path = "VCR_OSD_MONO.ttf"
        self.initialized = False
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.game.running = False
    def update(self, blinked=False):
        if not self.initialized:
            self.setup()
            self.initialized = True

    def render(self):
        pass

    def setup(self):
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

class SplashScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.caption_1_x = self.game.SCREEN_WIDTH * 2
        self.caption_2_x = int(-self.game.SCREEN_WIDTH * 1.5)
        self.caption_3_y = 0
    def update(self, blinked):
        self.caption_1_x -= 5
        self.caption_2_x += 5
        if self.caption_3_y < self.game.SCREEN_HEIGHT / 5 * 4:
            self.caption_3_y += 5
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "START"
    def render(self):
        self.game.screen.fill("black")
        self.draw_text("GLEB GAEVOY PRESENTS...", self.caption_1_x, self.game.SCREEN_HEIGHT // 2 - 75, 100)
        self.draw_text("EYERHYTHM (prototype)", self.caption_2_x, self.game.SCREEN_HEIGHT // 2 + 25, 100)
        self.draw_text("Press SPACE to skip.", self.game.SCREEN_WIDTH // 2, self.caption_3_y, 40)

class StartState(BaseState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "CALIBRATION"

    def update(self, blinked):
        pygame.mixer.music.fadeout(3000)

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
            self.game.state = "DIFFICULTYSELECTION"

    def update(self, blinked):
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

        #for the counter
        self.r_val = 255
        self.g_val = 0

        self.yellow_flag = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.blink_cnt >= 10: #try to make it automatic
            self.game.state = "TUTORIAL"
        super().handle_events(event)

    def update(self, blinked):
        if blinked:
            self.blink_cnt += 1
            print(self.blink_cnt, self.blink_cnt >= 10)

            if not self.yellow_flag:
                self.g_val += 85
            else:
                self.r_val -= 85

            if self.g_val >= 255:
                self.g_val = 255
                self.yellow_flag = True

            if self.r_val < 0:
                self.r_val = 0

    def render(self):
        self.game.screen.fill((40, 130, 255))

        title = "CALIBRATION"
        self.draw_text(title, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 8, 100)

        subtitle = f"look into the camera and blink at least 10 times. Then press SPACE."

        self.draw_text(subtitle, self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 3, 25)

        self.draw_text(str(self.blink_cnt), self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 3 * 2, 150, color=(self.r_val, self.g_val, 0))

class DifficultySelection(BaseState):
    def __init__(self, game):
        super().__init__(game)

        #UI
        self.continue_button = Button(self.game.screen, (self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 5 * 4), (500, 100), "cyan", text="CONTINUE")

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.state = "GAMEPLAY"
        if self.continue_button.is_clicked(event):
            self.game.state = "GAMEPLAY"

        super().handle_events(event)

    def update(self, blinked=False):
        pass

    def render(self):
        self.game.screen.fill("blue")
        self.draw_text("DIFFICULTY SELECTION", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 5, 50, "red")
        self.draw_text("NOT DONE YET :) just press the button below.", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 5 * 3, 30)
        self.continue_button.draw()
        #buttons: speed, needed_score, game_mode maybe even


class GameplayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.hits = 0
        self.misses = 0
        self.beatcnt = 0
        self.total_blinks = 0

        self.win_amm = 10
        self.lose_amm = 3

        self.misses_in_a_row = 0

        #GUI
        self.rball = RythmBall(self.game.screen, (self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2))
        self.ballsize = 1000

        #SFX
        self.hit_sfx = pygame.mixer.Sound("hit_sfx.mp3")
        self.miss_sfx = pygame.mixer.Sound("miss_sfx.mp3")

        #LOGIC
        self.beat_interval = 2000
        self.win_score = 5
        self.next_beat_time = pygame.time.get_ticks() + self.beat_interval
        self.hit = None

        self.level_finished = False

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.level_finished: #try to make it automatic
            self.game.state = "END"

    def update(self, blinked=False):
        if not self.level_finished:
            current_time = pygame.time.get_ticks()

            if current_time >= self.next_beat_time:
                self.next_beat_time += self.beat_interval
                self.beatcnt += 1

            if blinked:
                if self.next_beat_time - 200 <= current_time <= self.next_beat_time + 200: #change 200 to precision window from configs
                    self.hits += 1
                    self.hit = True
                    self.hit_sfx.play()
                    print("HIT!", self.hits)
                else:
                    self.misses += 1
                    self.hit = False
                    self.miss_sfx.play()
                    print("MISS!", self.misses)

            self.ball_size = abs(self.next_beat_time - current_time)

        if self.hits >= self.win_score:
            self.level_finished = True

    def render(self):
        current_time = pygame.time.get_ticks()
        label_size = abs(self.next_beat_time - current_time) / self.beat_interval
        print(label_size)

        if not self.level_finished:
            self.game.screen.fill((255, 255, 255))
            self.rball.draw(self.ball_size)

            if self.hit is not None:
                if self.hit:
                    self.draw_text(f"HIT!", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2 - 30, int(30 * label_size), "green")
                else:
                    self.draw_text(f"MISS!", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2 - 30, int(30 * label_size), "red")
            self.draw_text(f"Objective: score {self.win_score}", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2, 20, "yellow")
            self.draw_text(f"score: {self.hits}", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2 + 25, 15)
        else:
            self.game.screen.fill((0, 255, 0))
            self.draw_text("LEVEL COMPLETED! press space to continue", self.game.SCREEN_WIDTH // 2, 100, 20)


class EndState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.sound_played = False

    def setup(self):
        win_sfx = pygame.mixer.Sound("win_sfx.mp3")
        if not self.sound_played:
            win_sfx.play()
            self.sound_played = True

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # try to make it automatic
            self.game.state = "START"

    def update(self, blinked=False):
        self.setup()

    def render(self):
        self.game.screen.fill((255, 255, 0))
        # Draw game over elements here
        self.draw_text("THE END. yay1!11!", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 4, 100, "black")
        self.draw_text("pls give feedback :3", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 6 * 4, 50, "red")
        self.draw_text("Press q to quit.   Press r to restart. (buggy)", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 6 * 5, 25, "Black")

        self.draw_image("feedback_qr.png", self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2)
