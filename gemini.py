import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Dino properties
dino_x = 50
dino_y = 400
dino_width = 40
dino_height = 60
dino_y_velocity = 0
gravity = 1
is_jumping = False

# Cactus properties
cactus_x = 800
cactus_y = 400
cactus_width = 30
cactus_height = 60
cactus_speed = 5

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over = False

# Dino jump function
def dino_jump():
    global is_jumping, dino_y_velocity
    if not is_jumping:
        is_jumping = True
        dino_y_velocity = -20

# Cactus generation
def generate_cactus():
    global cactus_x
    cactus_x = SCREEN_WIDTH + random.randint(0, 300)

# Collision detection
def check_collision(dino_x, dino_y, dino_width, dino_height, cactus_x, cactus_y, cactus_width, cactus_height):
    if dino_x < cactus_x + cactus_width and dino_x + dino_width > cactus_x and dino_y < cactus_y + cactus_height and dino_y + dino_height > cactus_y:
        return True
    return False

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                dino_jump()
            if event.key == pygame.K_r and game_over:
                # Reset the game
                game_over = False
                dino_y = 400
                dino_y_velocity = 0
                is_jumping = False
                cactus_x = 800
                score = 0

    # Game logic
    if not game_over:
        # Dino movement
        dino_y += dino_y_velocity
        dino_y_velocity += gravity
        if dino_y >= 400:
            dino_y = 400
            is_jumping = False

        # Cactus movement
        cactus_x -= cactus_speed
        if cactus_x < -cactus_width:
            generate_cactus()
            score += 1

        # Collision detection
        if check_collision(dino_x, dino_y, dino_width, dino_height, cactus_x, cactus_y, cactus_width, cactus_height):
            game_over = True

    # Drawing
    screen.fill(WHITE)

    # Draw dino
    pygame.draw.rect(screen, GREEN, (dino_x, dino_y, dino_width, dino_height))

    # Draw cactus
    pygame.draw.rect(screen, BLACK, (cactus_x, cactus_y, cactus_width, cactus_height))

    # Display score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 18))

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.delay(20)

# Quit Pygame
pygame.quit()