import sys
import pygame
import random

# Intializing PyGame Engine
pygame.init()

# Defining Constants
game_width = 1200
game_height = 600
fps = 60
black_color = (0, 0, 0)
green_color = (0, 255, 0)

# Initializing Images
try:
    cactus = pygame.image.load("cactus_bricks.png")
    fire = pygame.image.load("fire_bricks.png")
    dragon = pygame.image.load("dragon.png")
    flame = pygame.image.load("fireball.png")
    mario = pygame.image.load("maryo.png")
    start = pygame.image.load("start.png")
    end = pygame.image.load("end.png")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    sys.exit()
cactus_rect = cactus.get_rect()
cactus_rect.left = 0
fire_rect = fire.get_rect()
fire_rect.left = 0
fire_rect.top = game_height - fire_rect.height

font = pygame.font.SysFont("forte", 20)

canvas = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("High Seas Mario Game")

# Intializing Conditions
clock = pygame.time.Clock()
level = 1
score = 0


class Topscore:
    def __init__(self):
        self.high_score = 0

    def update(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score


topscore = Topscore()


class Dragon:
    velocity = level * 2

    def __init__(self):
        self.image = dragon
        self.rect = self.image.get_rect()
        self.rect.width -= 10
        self.rect.height -= 10
        self.rect.top = game_height // 2
        self.rect.right = game_width
        self.up = True
        self.down = False

    def update(self):
        if self.rect.top <= cactus_rect.bottom:
            self.up = False
            self.down = True
        elif self.rect.bottom >= fire_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.rect.top -= self.velocity
        elif self.down:
            self.rect.top += self.velocity

        canvas.blit(self.image, self.rect)


class Flame:
    velocity = 5

    def __init__(self, x, y):
        self.image = pygame.transform.scale(flame, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.top = y

    def update(self):
        self.rect.left -= self.velocity
        canvas.blit(self.image, self.rect)


class Mario:
    velocity = 5

    def __init__(self):
        self.image = mario
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = game_height // 2
        self.up = False
        self.down = True

    def update(self):
        if self.up and self.rect.top > cactus_rect.bottom:
            self.rect.top -= self.velocity
        if self.down and self.rect.bottom < fire_rect.top:
            self.rect.top += self.velocity
        canvas.blit(self.image, self.rect)


def game_over():
    pygame.mixer.music.stop()
    print("Game Over! Restarting...")
    topscore.update(score)
    canvas.fill(black_color)
    canvas.blit(end, end.get_rect(center=(game_width // 2, game_height // 2)))
    pygame.display.update()
    pygame.time.wait(2000)
    start_game()


def start_game():
    global SCORE, LEVEL

    SCORE = 0
    LEVEL = 1

    mario = Mario()
    dragon = Dragon()
    flames = []
    flame_timer = 0

    pygame.mixer.music.load("mario_theme.wav")
    pygame.mixer.music.play(-1)

    while True:
        canvas.fill(black_color)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mario.up = True
                    mario.down = False
                elif event.key == pygame.K_DOWN:
                    mario.down = True
                    mario.up = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    mario.up = False
                    mario.down = True
                elif event.key == pygame.K_DOWN:
                    mario.down = True
                    mario.up = False

        # Update Level and Obstacles
        if SCORE in range(0, 10):
            cactus_rect.bottom = 50
            fire_rect.top = game_height - 50
            LEVEL = 1
        elif SCORE in range(10, 20):
            cactus_rect.bottom = 100
            fire_rect.top = game_height - 100
            LEVEL = 2
        elif SCORE > 20:
            cactus_rect.bottom = 150
            fire_rect.top = game_height - 150
            LEVEL = 3

        # Dragon and Flame Logic
        dragon.update()
        flame_timer += 1
        if random.randint(1, 50)>49:
            flames.append(Flame(dragon.rect.left, dragon.rect.top + 30))
            flame_timer = 0

        for flame in flames[:]:
            flame.update()
            if flame.rect.right < 0:
                flames.remove(flame)
                SCORE += 1

        # Collision Detection
        for flame in flames:
            if flame.rect.colliderect(mario.rect):
                game_over()

        # Check for Mario touching the ceiling or floor
        if mario.rect.top <= cactus_rect.bottom or mario.rect.bottom >= fire_rect.top:
            game_over()

        # Draw Elements
        canvas.blit(cactus, cactus_rect)
        canvas.blit(fire, fire_rect)

        mario.update()

        # Display Score and Level
        score_text = font.render(f"Score: {SCORE}", True, green_color)
        level_text = font.render(f"Level: {LEVEL}", True, green_color)
        top_score_text = font.render(
            f"Top Score: {topscore.high_score}", True, green_color
        )
        canvas.blit(score_text, (50, 10))
        canvas.blit(level_text, (250, 10))
        canvas.blit(top_score_text, (450, 10))

        pygame.display.update()
        clock.tick(fps)


# Start the Game
start_game()
