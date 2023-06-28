import pygame
import sys
import random

def spawn_pipe():
    random_pipe_pos = random.choice(range(200, 350))
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos, 52, 320)
    top_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos - 150 - 320, 52, 320)
    return bottom_pipe, top_pipe

def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def update_score(pipes, score, passed_pipe):
    for pipe in pipes:
        if pipe.centerx < bird_rect.centerx and not passed_pipe:
            score += 1
            passed_pipe = True
        elif pipe.centerx > bird_rect.centerx:
            passed_pipe = False
    return score, passed_pipe

def draw_score(score):
    score_surface = game_font.render(str(score), True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

def game_over_screen():
    game_over_surface = game_font.render("Game Over", True, WHITE)
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.update()
    pygame.time.delay(1500)

def reset_game():
    global bird_rect, pipe_list, bird_movement, score, passed_pipe
    bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, bird_radius * 2, bird_radius * 2)
    pipe_list = []
    bird_movement = 0
    score = 0
    passed_pipe = False

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Game variables
gravity = 0.25
bird_movement = 0

game_font = pygame.font.Font(None, 40)
score = 0
passed_pipe = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

bird_radius = 16
bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, bird_radius * 2, bird_radius * 2)

pipe_list = []
PIPE_SPAWN_INTERVAL = 1200

spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, PIPE_SPAWN_INTERVAL)

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                reset_game()

        if event.type == spawn_pipe_event:
            pipe_list.extend(spawn_pipe())

    screen.fill(SKY_BLUE)

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        pygame.draw.circle(screen, YELLOW, bird_rect.center, bird_radius)

        pipe_list = [pipe.move(-5, 0) for pipe in pipe_list]
        for pipe in pipe_list:
            if pipe.right <= 0:
                pipe_list.remove(pipe)
            pygame.draw.rect(screen, GREEN, pipe)
            flipped_pipe = pipe.copy()
            flipped_pipe.height = -flipped_pipe.height
            flipped_pipe.top += 150
            pygame.draw.rect(screen, GREEN, flipped_pipe)

        # Check for collision
        if check_collision(bird_rect, pipe_list):
            game_active = False
            game_over_screen()

        # Update score
        score, passed_pipe = update_score(pipe_list, score, passed_pipe)

        # Draw score
        draw_score(score)

    pygame.display.update()
    clock.tick(FPS)

