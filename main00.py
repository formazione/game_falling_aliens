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
basket_speed = 10

# Basket movement
def move_basket(keys, basket_x):
    if keys[pygame.K_LEFT] and basket_rect.x > 0:
        basket_rect.x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_rect.x < SCREEN_WIDTH - basket_width:
        basket_rect.x += basket_speed
    return basket_rect.x

# Main game loop
running = True
basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    basket_rect.x = move_basket(keys, basket_rect.x)

    # Fill the screen with a color
    screen.fill(WHITE)

    # Draw the basket
    pygame.draw.rect(screen, BLACK, basket_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

pygame.quit()
