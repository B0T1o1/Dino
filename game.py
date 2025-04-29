import pygame
from pygame.locals import *
import random
import time

pygame.init()
screen = pygame.display.set_mode((1200, 400))

# Load and scale images
dino0 = pygame.image.load('dino0.png').convert_alpha()
dino1 = pygame.image.load('dino1.png').convert_alpha()
dino1 = pygame.transform.scale(dino1, (dino1.get_width()*2, dino1.get_height()*2))
dino2 = pygame.image.load('dino2.png').convert_alpha()
dino2 = pygame.transform.scale(dino2, (dino2.get_width()*2, dino2.get_height()*2))
dinojump = pygame.image.load('dinojump.png').convert_alpha()
dinojump = pygame.transform.scale(dinojump, (dinojump.get_width()*2, dinojump.get_height()*2))
dinocrouch = pygame.image.load('dinocrouch.png').convert_alpha()
dinocrouch = pygame.transform.scale(dinocrouch, (dinocrouch.get_width()*2, dinocrouch.get_height()*2))

ground = pygame.image.load('ground.png').convert_alpha()
ground = pygame.transform.scale(ground, (ground.get_width()*5, ground.get_height()))

cactus = pygame.image.load('cactus.png').convert_alpha()
cactus = pygame.transform.scale(cactus, (cactus.get_width()*1.7, cactus.get_height()*1.7))

bird = pygame.image.load('bird.png').convert_alpha()
bird = pygame.transform.scale(bird, (bird.get_width()*2, bird.get_height()*2))

font = pygame.font.SysFont("Arial", 20)

running = True
clock = pygame.time.Clock()

y = 300
y_of_dino = 300
evens = 1000

velocity_of_y = 0
gravity = 2
ground_pos = 0
ground_velocity = 10
crouched = False

show_rects = True  # Toggle for showing collision rects

# Obstacle class
class obstacle:
    def __init__(self, x, surface, name, height):
        self.x = x
        self.surface = surface
        self.name = name
        self.height = height

    def move(self, ground_velocity):
        self.x -= ground_velocity

    def get_rect(self):
        return pygame.Rect(self.x + self.surface.get_width()/4, y -self.height +self.surface.get_height()/2 + 5, self.surface.get_width()/2, self.surface.get_height()/2)

# Create initial obstacles
currentobstacles = [
    obstacle(1300, cactus, 'cactus', 60),
    obstacle(1600, cactus, 'cactus', 60),
    obstacle(1900, cactus, 'cactus', 60)
]

changing = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                show_rects = not show_rects  # Toggle rectangle visibility

    keys = pygame.key.get_pressed()
    if keys[K_SPACE] and y_of_dino == 300:
        velocity_of_y = 14
    if keys[K_UP] and y_of_dino == 300:
        velocity_of_y = 16
    if keys[K_DOWN]:
        crouched = True
    else:
        crouched = False

    y_of_dino -= velocity_of_y
    if y_of_dino < 300:
        velocity_of_y -= gravity * (2 if crouched else 1)
    else:
        velocity_of_y = 0
        y_of_dino = 300

    ground_pos -= ground_velocity
    evens += 1
    if ground_pos < -256*5:
        ground_pos = 0

    screen.fill((255, 255, 255))
    screen.blit(ground, (ground_pos, y - 71))
    screen.blit(ground, (ground_pos + 256*5, y - 71))

    # Select current dino sprite
    if crouched:
        current_dino = dinocrouch
    elif y_of_dino != 300:
        current_dino = dinojump
    elif evens % 4 > 2:
        current_dino = dino1
    else:
        current_dino = dino2

    dino_rect = pygame.Rect(15 + current_dino.get_width()/4, y_of_dino+current_dino.get_height()/5, current_dino.get_width()/2, current_dino.get_height()/2)
    screen.blit(current_dino, (15, y_of_dino))

    # Move and draw obstacles
    for i, obs in enumerate(currentobstacles):
        obs.move(ground_velocity)

        if obs.x < -10:
            obs_type = random.choice(['cactus', 'bird'])
            if obs_type == 'cactus':
                currentobstacles[i] = obstacle(1300, cactus, 'cactus', 60)
            else:
                currentobstacles[i] = obstacle(1300, bird, 'bird', random.randint(15, 70))
            continue

        obs_rect = obs.get_rect()
        if obs_rect.colliderect(dino_rect):
            running = False

        screen.blit(obs.surface, (obs.x, y - obs.height))

        if show_rects:
            pygame.draw.rect(screen, (0, 0, 255), obs_rect, 2)  # Blue for obstacles

    if show_rects:
        pygame.draw.rect(screen, (255, 0, 0), dino_rect, 2)  # Red for dino

    # Draw score
    score = evens
    text_surface = font.render(str(score), True, (123, 129, 126))
    screen.blit(text_surface, (1100, 5))

    if score > 1000:
        ground_velocity = score / 100
        changing = True

    pygame.display.flip()
    clock.tick(40)

# Game over screen
over_surface = font.render('Game Over!', True, (123, 129, 126))
screen.blit(over_surface, (300, 200))
pygame.display.flip()

time.sleep(20)
pygame.quit()
 