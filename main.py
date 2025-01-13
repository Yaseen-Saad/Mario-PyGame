import sys
import pygame
import os
import pygame

# Ensure compatibility
base_path = os.path.dirname(__file__)

# Initialize Pygame Engine
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60
COLORS = {
    "black": (0, 0, 0),
    "green": (0, 255, 0),
}

# Load Images with Error Handling
def load_image(file):
    try:
        return pygame.image.load(file)
    except pygame.error as e:
        print(f"Error loading {file}: {e}")
        sys.exit()

IMG_CACTUS = load_image(os.path.join(base_path, "cactus_bricks.png"))
IMG_FIRE = load_image(os.path.join(base_path, "fire_bricks.png"))
IMG_FLAME = load_image(os.path.join(base_path, "fireball.png"))
IMG_MARIO = load_image(os.path.join(base_path, "maryo.png"))
IMG_START= load_image(os.path.join(base_path, "start.png"))
IMG_END = load_image(os.path.join(base_path, "end.png"))
IMG_HEART = load_image(os.path.join(base_path, "heart.png"))
IMG_DRAGON = load_image(os.path.join(base_path, "dragon.png"))

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("High Seas Mario")

# Clock for FPS Management
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont("forte", 20)

# High Score Tracker
class HighScore:
    def __init__(self):
        self.high_score = 0

    def update(self, current_score):
        if current_score > self.high_score:
            self.high_score = current_score

# Dragon Class
class Dragon:
    def __init__(self):
        self.image = IMG_DRAGON
        self.rect = self.image.get_rect()
        self.rect.width -= 10
        self.rect.height -= 10
        self.rect.top = SCREEN_HEIGHT // 2
        self.rect.right = SCREEN_WIDTH
        self.movement_speed = 2
        self.moving_up = True

    def update(self, level):
        self.movement_speed = level * 2
        if self.rect.top <= cactus_rect.bottom:
            self.moving_up = False
        elif self.rect.bottom >= fire_rect.top:
            self.moving_up = True

        self.rect.top -= self.movement_speed if self.moving_up else -self.movement_speed
        screen.blit(self.image, self.rect)

# Flame Class
class Flame:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(IMG_FLAME, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.top = y
        self.movement_speed = 5

    def update(self):
        self.rect.left -= self.movement_speed
        screen.blit(self.image, self.rect)

# Mario Class
class Mario:
    def __init__(self):
        self.image = IMG_MARIO
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = SCREEN_HEIGHT // 2
        self.movement_speed = 5
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up and self.rect.top > cactus_rect.bottom:
            self.rect.top -= self.movement_speed
        if self.moving_down and self.rect.bottom < fire_rect.top:
            self.rect.top += self.movement_speed
        screen.blit(self.image, self.rect)

# Game Over Function
def game_over(high_score_tracker, score):
    pygame.mixer.music.stop()
    high_score_tracker.update(score)
    screen.fill(COLORS["black"])
    screen.blit(
        IMG_END, IMG_END.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    )
    pygame.display.update()
    pygame.time.wait(2000)

# Main Game Function
def main_game():
    # Game Variables
    score = 0
    level = 1
    lives = 3
    high_score_tracker = HighScore()

    # Obstacle Rectangles
    global cactus_rect, fire_rect
    cactus_rect = IMG_CACTUS.get_rect()
    cactus_rect.left = 0
    fire_rect = IMG_FIRE.get_rect()
    fire_rect.left = 0
    fire_rect.top = SCREEN_HEIGHT - fire_rect.height

    # Game Objects
    player = Mario()
    enemy = Dragon()
    flames = []

    pygame.mixer.music.load("mario_theme.wav")
    pygame.mixer.music.play(-1)

    flame_spawn_timer = 0
    running = True

    while running:
        screen.fill(COLORS["black"])

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.moving_up = True
                elif event.key == pygame.K_DOWN:
                    player.moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.moving_up = False
                elif event.key == pygame.K_DOWN:
                    player.moving_down = False

        # Update Level Based on Score
        if score < 10:
            level = 1
            cactus_rect.bottom = 50
            fire_rect.top = SCREEN_HEIGHT - 50
        elif score < 20:
            level = 2
            cactus_rect.bottom = 100
            fire_rect.top = SCREEN_HEIGHT - 100
        else:
            level = 3
            cactus_rect.bottom = 150
            fire_rect.top = SCREEN_HEIGHT - 150

        # Update Enemy
        enemy.update(level)

        # Flame Logic
        flame_spawn_timer += 1
        if flame_spawn_timer > 50:
            flames.append(Flame(enemy.rect.left, enemy.rect.top + 30))
            flame_spawn_timer = 0

        for flame in flames[:]:
            flame.update()
            if flame.rect.right < 0:
                flames.remove(flame)
                score += 1

        # Collision Detection
        for flame in flames[:]:
            if flame.rect.colliderect(player.rect):
                flames.remove(flame)
                lives -= 1
                if lives <= 0:
                    game_over(high_score_tracker, score)
                    return

        if player.rect.top <= cactus_rect.bottom or player.rect.bottom >= fire_rect.top:
            lives -= 1
            if lives <= 0:
                game_over(high_score_tracker, score)
                return

        # Draw Scene
        screen.blit(IMG_CACTUS, cactus_rect)
        screen.blit(IMG_FIRE, fire_rect)
        player.update()

        # Display HUD
        score_text = FONT.render(f"Score: {score}", True, COLORS["green"])
        level_text = FONT.render(f"Level: {level}", True, COLORS["green"])
        top_score_text = FONT.render(
            f"High Score: {high_score_tracker.high_score}", True, COLORS["green"]
        )
        lives_text = FONT.render(f"Lives: {lives}", True, COLORS["green"])

        screen.blit(score_text, (50, 10))
        screen.blit(level_text, (250, 10))
        screen.blit(top_score_text, (450, 10))
        screen.blit(lives_text, (650, 10))

        pygame.display.update()
        clock.tick(FPS)

# Start the Game
main_game()
