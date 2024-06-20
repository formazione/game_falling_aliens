import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Basket properties
basket_width = 100
basket_height = 20
basket_x = (SCREEN_WIDTH - basket_width) // 2
basket_y = SCREEN_HEIGHT - basket_height - 10
basket_speed = 20

# Object properties
object_width = 30
object_height = 30
object_speed = 2

# Create multiple objects
num_objects = 3
objects = [{'x': random.randint(0, SCREEN_WIDTH - object_width), 'y': -object_height} for _ in range(num_objects)]

# Basket movement
def move_basket(keys, basket_x):
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
        basket_x += basket_speed
    return basket_x

# Check for collision
def check_collision(basket_x, basket_y, object_x, object_y):
    if (object_x < basket_x + basket_width and
        object_x + object_width > basket_x and
        object_y < basket_y + basket_height and
        object_y + object_height > basket_y):
        return True
    return False

# Main game loop
running = True
score = 0
lives = 3
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    basket_x = move_basket(keys, basket_x)

    # Move the objects
    for obj in objects:
        obj['y'] += object_speed
        if obj['y'] > SCREEN_HEIGHT:
            obj['y'] = -object_height
            obj['x'] = random.randint(0, SCREEN_WIDTH - object_width)
            lives -= 1

        # Check for collision
        if check_collision(basket_x, basket_y, obj['x'], obj['y']):
            score += 1
            obj['y'] = -object_height
            obj['x'] = random.randint(0, SCREEN_WIDTH - object_width)

    if lives <= 0:
        running = False

    # Fill the screen with a color
    screen.fill(WHITE)

    # Draw the basket
    pygame.draw.rect(screen, BLACK, (basket_x, basket_y, basket_width, basket_height))

    # Draw the objects
    for obj in objects:
        pygame.draw.rect(screen, RED, (obj['x'], obj['y'], object_width, object_height))

    # Display the score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
