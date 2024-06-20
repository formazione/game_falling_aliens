import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BULLET_SPEED = 10
PAUSE_DURATION = 1  # Pause duration in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Falling Aliens")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Basket properties
basket_width = 100
basket_height = 20
basket_x = (SCREEN_WIDTH - basket_width) // 2
basket_y = SCREEN_HEIGHT - basket_height - 10
basket_speed = 10

# Load sprite sheet and split into individual images
def load_spritesheet(filename, sprite_width, sprite_height, num_sprites):
    sheet = pygame.image.load(filename).convert_alpha()
    sprites = []
    for i in range(num_sprites):
        rect = pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height)
        image = sheet.subsurface(rect)
        sprites.append(image)
    return sprites

# Load alien images from sprite sheet
alien_images = load_spritesheet('aliens_spritesheet2.png', 30, 30, 3)
alien_width = alien_images[0].get_width()
alien_height = alien_images[0].get_height()

# Object properties
base_speed = 3
initial_aliens = 10

# Create initial objects
def create_aliens(num_aliens):
    return [{'x': random.randint(0, SCREEN_WIDTH - alien_width), 
             'y': -alien_height, 
             'image': random.choice(alien_images), 
             'speed_x': random.choice([-1, 0, 1]) * random.randint(1, 3), 
             'speed_y': random.randint(base_speed, base_speed + 3)} for _ in range(num_aliens)]

objects = create_aliens(initial_aliens)
bullets = []

# Basket movement
def move_basket(keys, basket_x):
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
        basket_x += basket_speed
    return basket_x

# Check for collision with basket
def check_collision(basket_x, basket_y, object_x, object_y):
    if (object_x < basket_x + basket_width and
        object_x + alien_width > basket_x and
        object_y < basket_y + basket_height and
        object_y + alien_height > basket_y):
        return True
    return False

# Check for collision between two objects
def check_object_collision(obj1, obj2):
    if (obj1['x'] < obj2['x'] + alien_width and
        obj1['x'] + alien_width > obj2['x'] and
        obj1['y'] < obj2['y'] + alien_height and
        obj1['y'] + alien_height > obj2['y']):
        return True
    return False

# Add a new alien
def add_new_alien():
    new_alien = {
        'x': random.randint(0, SCREEN_WIDTH - alien_width),
        'y': -alien_height,
        'image': random.choice(alien_images),
        'speed_x': random.choice([-1, 0, 1]) * random.randint(1, 3),
        'speed_y': random.randint(base_speed, base_speed + 3)
    }
    objects.append(new_alien)

# Main game loop
running = True
game_over = False
score = 0
lives = 3
start_time = time.time()
aliens_off_screen = 0
current_scene_aliens = initial_aliens

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            game_over = False
            score = 0
            lives = 3
            aliens_off_screen = 0
            current_scene_aliens = initial_aliens
            objects = create_aliens(initial_aliens)
            bullets = []
            start_time = time.time()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x and not game_over:
            bullet_x = basket_x + basket_width // 2
            bullet_y = basket_y
            bullets.append({'x': bullet_x, 'y': bullet_y})

    if game_over:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, BLACK)
        instruction_text = font.render("Press any key to start again", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - instruction_text.get_height() // 2 + 50))
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    basket_x = move_basket(keys, basket_x)

    # Move the objects
    current_time = time.time()
    time_elapsed = current_time - start_time

    for obj in objects:
        obj['x'] += obj['speed_x']
        obj['y'] += obj['speed_y'] + time_elapsed * 0.01  # Increase speed over time
        
        if obj['x'] < 0 or obj['x'] > SCREEN_WIDTH - alien_width:
            obj['speed_x'] *= -1

        if obj['y'] > SCREEN_HEIGHT:
            objects.remove(obj)
            aliens_off_screen += 1
            score += 1  # Increase score when the object safely passes

        # Check for collision with basket
        if check_collision(basket_x, basket_y, obj['x'], obj['y']):
            lives -= 1
            objects.remove(obj)

    # Check for collisions between objects
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if check_object_collision(objects[i], objects[j]):
                objects[i]['speed_x'], objects[j]['speed_x'] = objects[j]['speed_x'], objects[i]['speed_x']
                objects[i]['speed_y'], objects[j]['speed_y'] = objects[j]['speed_y'], objects[i]['speed_y']
                add_new_alien()

    # Move and check bullets
    for bullet in bullets:
        bullet['y'] -= BULLET_SPEED
        if bullet['y'] < 0:
            bullets.remove(bullet)
        for obj in objects:
            if check_collision(bullet['x'], bullet['y'], obj['x'], obj['y']):
                objects.remove(obj)
                if bullet in bullets:
                    bullets.remove(bullet)
                score += 1
                break

    if lives <= 0:
        game_over = True

    if aliens_off_screen >= 10:
        aliens_off_screen = 0
        current_scene_aliens += 5
        time.sleep(PAUSE_DURATION)
        objects = create_aliens(current_scene_aliens)

    # Fill the screen with a color
    screen.fill(WHITE)

    # Draw the basket
    pygame.draw.rect(screen, BLACK, (basket_x, basket_y, basket_width, basket_height))

    # Draw the objects
    for obj in objects:
        screen.blit(obj['image'], (obj['x'], obj['y']))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, (bullet['x'], bullet['y'], 5, 10))

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
