import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Runner")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the ground dimensions
ground_width = window_width
ground_height = 50

# Set up the dinosaur dimensions
dinosaur_width = 50
dinosaur_height = 50
dinosaur_x = 50
dinosaur_y = window_height - ground_height - dinosaur_height
dinosaur_velocity = 5
dinosaur_dx = 0

# Set up game variables
jumping = False
jump_count = 10
score = 0
game_over = False
game_over_timer = 0
clock = pygame.time.Clock()

# Particle effect variables
particles = []
particle_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0)]
max_particles = 100
particle_radius = 3

# Obstacle class
class Obstacle:
    def __init__(self):
        self.height = random.randint(dinosaur_height // 2, dinosaur_height)
        self.width = random.randint(self.height // 2, dinosaur_height // 2)
        self.x = window_width
        self.y = window_height - ground_height - self.height
        self.velocity = 5  # Same velocity for all obstacles
        self.passed = False

    def update(self):
        self.x -= self.velocity

    def draw(self):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height))

    def collides_with(self, rect):
        return self.x < rect.x + rect.width and self.x + self.width > rect.x and \
               self.y < rect.y + rect.height and self.y + self.height > rect.y


# Create obstacles list
obstacles = []

# Function to create particle effect
def create_particles(position):
    particle_count = random.randint(20, 30)
    for _ in range(particle_count):
        dx = random.randint(-5, 5)
        dy = random.randint(-15, -5)
        color = random.choice(particle_colors)
        particles.append([position[0], position[1], dx, dy, color])


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping and not game_over:
                jumping = True
            elif event.key == pygame.K_LEFT and not game_over:
                dinosaur_dx = -dinosaur_velocity
            elif event.key == pygame.K_RIGHT and not game_over:
                dinosaur_dx = dinosaur_velocity
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and not game_over:
                dinosaur_dx = 0
            elif event.key == pygame.K_RIGHT and not game_over:
                dinosaur_dx = 0
            elif event.key == pygame.K_SPACE and game_over:
                # Restart the game
                game_over = False
                score = 0
                dinosaur_x = 50
                dinosaur_y = window_height - ground_height - dinosaur_height
                obstacles = []
                game_over_timer = 0
                particles.clear()

    # Update game logic
    if jumping:
        if jump_count >= -10:
            dinosaur_y -= jump_count * abs(jump_count) * 0.5
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    if not game_over:
        # Update dinosaur position
        dinosaur_x += dinosaur_dx

        # Prevent the player from leaving the screen
        if dinosaur_x < 0:
            dinosaur_x = 0
        elif dinosaur_x + dinosaur_width > window_width:
            dinosaur_x = window_width - dinosaur_width

        # Update obstacle positions
        for obstacle in obstacles:
            obstacle.update()

            # Check for collision
            if obstacle.collides_with(pygame.Rect(dinosaur_x, dinosaur_y, dinosaur_width, dinosaur_height)):
                game_over = True
                create_particles((dinosaur_x + dinosaur_width // 2, dinosaur_y + dinosaur_height // 2))
                game_over_timer = pygame.time.get_ticks()

            # Check if obstacle passed the player
            if not obstacle.passed and obstacle.x + obstacle.width < dinosaur_x:
                obstacle.passed = True
                score += 1

        # Generate new obstacles
        if len(obstacles) == 0 or obstacles[-1].x < window_width - random.randint(200, 400):
            obstacles.append(Obstacle())

        # Remove off-screen obstacles
        if obstacles and obstacles[0].x + obstacles[0].width < 0:
            obstacles.pop(0)

    # Draw game elements
    window.fill(WHITE)

    # Draw ground
    pygame.draw.rect(window, BLACK, (0, window_height - ground_height, ground_width, ground_height))

    # Draw dinosaur
    pygame.draw.rect(window, BLACK, (dinosaur_x, dinosaur_y, dinosaur_width, dinosaur_height))

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw()

    # Particle effect
    for particle in particles:
        pygame.draw.circle(window, particle[4], (int(particle[0]), int(particle[1])), particle_radius)
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[3] += 0.5  # Gravity
        if particle[1] >= window_height:
            particles.remove(particle)

    if game_over:
        if pygame.time.get_ticks() - game_over_timer > 1000:
            # Display "You Lose" message and fade-in effect
            alpha = min((pygame.time.get_ticks() - game_over_timer - 1000) // 2, 255)
            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            window.blit(overlay, (0, 0))
            font = pygame.font.Font(None, 72)
            text = font.render("You Lose", True, WHITE)
            text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
            window.blit(text, text_rect)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # Restart the game
            game_over = False
            score = 0
            dinosaur_x = 50
            dinosaur_y = window_height - ground_height - dinosaur_height
            obstacles = []
            game_over_timer = 0
            particles.clear()
    else:
        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, BLACK)
        window.blit(text, (10, 10))

    # Update the display
    pygame.display.update()
    clock.tick(30)

# Quit the game
pygame.quit()
