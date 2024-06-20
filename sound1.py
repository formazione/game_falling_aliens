import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sound in Pygame')

# Load sounds
pygame.mixer.music.load('background.wav')
jump_sound = pygame.mixer.Sound('jump.wav')
collision_sound = pygame.mixer.Sound('collision.wav')

# Play background music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Player attributes
player_size = 50
player_color = BLACK
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size
player_velocity = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_velocity > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x + player_velocity < SCREEN_WIDTH - player_size:
        player_x += player_velocity
    if keys[pygame.K_SPACE]:
        jump_sound.play()
        # Simulate jump by moving up and then down
        player_y -= 10
        pygame.time.delay(50)
        player_y += 10

    # Simulate collision
    if player_x < 100:  # Example condition for collision
        collision_sound.play()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Update the display
    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(30)
