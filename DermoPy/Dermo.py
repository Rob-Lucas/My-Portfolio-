import pygame
import random
import math
from pygame.locals import *

# Initialize Pygame
# pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1080 * 3/4 , 1080 * 3/4
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

ROTATION_SPEED = 2 #This is in Radians
PLAYER_RADIUS = 5
PROJECTILE_RADIUS = 3
ENEMY_RADIUS = 10
ENEMY_SPAWN_RATE = 100
ENEMY_SPEED_INCREMENT = 0.005
BACKGROUND_SPEED = 2
PROJECTILE_SPEED = 10
LASER_WIDTH = 1
MULTI_HIT_CHANCE = 0.2

# Start menu
def start_menu(screen):
    font = pygame.font.Font(None, 48)
    start_btn = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50)
    running = True
    start_game = False

    while running:
        screen.fill((0, 0, 0))

        # Draw the title text
        title_text = font.render("DERMO", True, WHITE, None)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        pygame.draw.rect(screen, GREEN, title_text_rect.inflate(6, 6), 3)
        screen.blit(title_text, title_text_rect)

        # Draw the start button
        pygame.draw.rect(screen, GREEN, start_btn, 3)
        button_text = font.render("Start", True, GREEN, None)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = start_btn.center
        screen.blit(button_text, button_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_game = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_btn.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, GREEN, start_btn)
                    screen.blit(button_text, button_text_rect)
                    pygame.display.flip()
                    pygame.time.delay(100)

                    # Play a low tone
                    # pygame.mixer.music.load('low_tone.wav')
                    # pygame.mixer.music.play(0)

                    running = False
                    start_game = True

        pygame.display.flip()
        clock.tick(60)

    return start_game

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Start menu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Shooter")
clock = pygame.time.Clock()
start_game = start_menu(screen)

if start_game:
    # Load and play music
    pygame.mixer.music.load('evolution.wav')
    pygame.mixer.music.play(-1)  # Play the music in a loop

    # Player class
    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.angle = 0

        def draw(self, screen):
            pygame.draw.circle(screen, GREEN, (self.x, self.y), PLAYER_RADIUS + 6, 1)
            pygame.draw.circle(screen, BLUE, (self.x, self.y), PLAYER_RADIUS + 6)

        def update(self, screen, keys):
            # Update angle based on arrow keys with smaller increments
            if keys[pygame.K_LEFT]:
                self.angle += math.radians(ROTATION_SPEED)
            if keys[pygame.K_RIGHT]:
                self.angle -= math.radians(ROTATION_SPEED)

            # Draw the laser line (screen-wide length)
            end_x = self.x + math.cos(self.angle) * SCREEN_WIDTH
            end_y = self.y - math.sin(self.angle) * SCREEN_WIDTH
            pygame.draw.line(screen, RED, (self.x, self.y), (end_x, end_y), LASER_WIDTH)

    # Projectile class
    class Projectile:
        def __init__(self, x, y, angle):
            self.x = x
            self.y = y
            self.angle = angle

        def draw(self, screen):
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), PROJECTILE_RADIUS)

        def update(self):
            self.x += math.cos(self.angle) * PROJECTILE_SPEED
            self.y -= math.sin(self.angle) * PROJECTILE_SPEED

    # Enemy class
    class Enemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.speed = random.uniform(1, 3)

        def draw(self, screen):
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), ENEMY_RADIUS)

        def update(self, player_x, player_y):
            angle = math.atan2(player_y - self.y, player_x - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed
    
    # class GoldEnemy(Enemy):
    #     def __init__(self, x, y):
    #         super(GoldEnemy, self).__init__(x, y)  # Update this line
    #         self.color = (255, 215, 0)

    # Collision detection
    def check_collision(x1, y1, r1, x2, y2, r2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= r1 + r2

     # Main game loop
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Shooter")
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    projectiles = []
    enemies = []
    enemy_spawn_timer = 0

    running = True
    space_pressed = False

    running = True
    last_gold_enemy_spawn_time = pygame.time.get_ticks()
    gold_enemy_spawn_interval = random.randint(15000, 50000)
    gold_enemy = None

    kill_count = 0
    font = pygame.font.Font(None, 36)
    text_color = (0, 255, 0)

    rapid_fire = False
    rapid_fire_start_time = None
    while running:
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks()
        all_sprites = pygame.sprite.Group()
        # Gradually increase enemy spawn rate
        enemy_spawn_interval = max(1000 - (current_time // 30000) * 500, 100)

        # # Spawn gold enemy
        # if (current_time - last_gold_enemy_spawn_time) > gold_enemy_spawn_interval and gold_enemy is None:
        #     gold_enemy = GoldEnemy(random.randint(0, SCREEN_WIDTH), -10)
        #     all_sprites.add(gold_enemy)
        #     enemies.add(gold_enemy)
        
        # Rapid fire ability duration
        if rapid_fire and (current_time - rapid_fire_start_time) > 15000:
            rapid_fire = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Shooting
        if keys[pygame.K_SPACE] and not space_pressed:
            projectiles.append(Projectile(player.x, player.y, player.angle))
            space_pressed = True
        elif not keys[pygame.K_SPACE]:
            space_pressed = False

        # Update and draw player
        player.update(screen, keys)
        player.draw(screen)

        # Update and draw projectiles
        for projectile in projectiles:
            projectile.update()
            projectile.draw(screen)

        # Update and draw enemies
        for enemy in enemies:
            enemy.update(player.x, player.y)
            enemy.draw(screen)

        # Collision detection and scoring
        remaining_projectiles = []

        for projectile in projectiles:
            hit = False
            new_enemies = []

            for enemy in enemies:
                if check_collision(projectile.x, projectile.y, PROJECTILE_RADIUS, enemy.x, enemy.y, ENEMY_RADIUS):
                    hit = True
                    if random.random() <= MULTI_HIT_CHANCE:
                        # Find the closest enemy behind the current one
                        min_distance = float('inf')
                        target = None

                        for e in enemies:
                            if e != enemy:
                                dx = e.x - enemy.x
                                dy = e.y - enemy.y
                                angle = math.atan2(dy, dx)
                                distance = math.sqrt(dx ** 2 + dy ** 2)

                                if abs(angle - math.atan2(player.y - enemy.y, player.x - enemy.x) - math.pi) < 0.3 and distance < min_distance:
                                    min_distance = distance
                                    target = e

                        if target:
                            projectile.x, projectile.y = enemy.x, enemy.y
                            projectile.angle = math.atan2(target.y - enemy.y, target.x - enemy.x)

                    else:
                        continue  # Skip this enemy, allowing the bullet to pass through
                new_enemies.append(enemy)

            if not hit:
                remaining_projectiles.append(projectile)

            enemies = new_enemies

        projectiles = remaining_projectiles

        # Enemy spawn rate and speed adjustment
        enemy_spawn_timer += 1

        if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            enemy_spawn_timer = 0
            spawn_side = random.choice(['top', 'bottom', 'left', 'right'])

            if spawn_side == 'top':
                spawn_x = random.randint(0, SCREEN_WIDTH)
                spawn_y = -ENEMY_RADIUS
            elif spawn_side == 'bottom':
                spawn_x = random.randint(0, SCREEN_WIDTH)
                spawn_y = SCREEN_HEIGHT + ENEMY_RADIUS
            elif spawn_side == 'left':
                spawn_x = -ENEMY_RADIUS
                spawn_y = random.randint(0, SCREEN_HEIGHT)
            elif spawn_side == 'right':
                spawn_x = SCREEN_WIDTH + ENEMY_RADIUS
                spawn_y = random.randint(0, SCREEN_HEIGHT)

            enemies.append(Enemy(spawn_x, spawn_y))
            ENEMY_SPAWN_RATE = max(10, ENEMY_SPAWN_RATE - 1)

            for enemy in enemies:
                enemy.speed += ENEMY_SPEED_INCREMENT

        pygame.display.flip()
        clock.tick(60)
        # Check for gold enemy collision
        if gold_enemy is not None and pygame.sprite.spritecollide(gold_enemy, projectiles, True):
            rapid_fire = True
            rapid_fire_start_time = current_time
            all_sprites.remove(gold_enemy)
            enemies.remove(gold_enemy)
            gold_enemy = None
            last_gold_enemy_spawn_time = current_time
            gold_enemy_spawn_interval = random.randint(15000, 50000)
            kill_count += 1

        # Display kill count
        text = font.render(f"Kills: {kill_count}", True, text_color)
        screen.blit(text, (10, 10))

    pygame.quit()
else:
    pygame.quit()