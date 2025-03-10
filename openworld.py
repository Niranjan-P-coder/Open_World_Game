import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_SIZE = 50
SQUARE_COLOR = (0, 128, 255)
BLOCK_COLOR = (255, 0, 0)
BLOCK_SIZE = 70
BACKGROUND_COLOR = (30, 30, 30)
MOVE_SPEED = 5
ENEMY_COLOR = (255, 255, 0)
ENEMY_SIZE = 40
ENEMY_SPEED = 2
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
MAX_HEALTH = 100

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Player position in the world
block_x, block_y = 0, 0

# Blocks
blocks = [[400, 300], [600, 400], [200, 500]]

# Health
health = MAX_HEALTH

# Enemies
enemies = []

def spawn_enemy():
    enemy_x = random.randint(-1000, 1000)
    enemy_y = random.randint(-1000, 1000)
    enemies.append([enemy_x, enemy_y])

# Spawn initial enemies
for _ in range(5):
    spawn_enemy()

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys
    keys = pygame.key.get_pressed()
    prev_x, prev_y = block_x, block_y
    
    # Move player in the world
    if keys[pygame.K_UP]:
        block_y -= MOVE_SPEED
    if keys[pygame.K_DOWN]:
        block_y += MOVE_SPEED
    if keys[pygame.K_LEFT]:
        block_x -= MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        block_x += MOVE_SPEED

    # Player collision with blocks
    player_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SQUARE_SIZE, SQUARE_SIZE)
    for block in blocks:
        block_rect = pygame.Rect(block[0] - block_x + SCREEN_WIDTH // 2, block[1] - block_y + SCREEN_HEIGHT // 2, BLOCK_SIZE, BLOCK_SIZE)
        if player_rect.colliderect(block_rect):
            block_x, block_y = prev_x, prev_y
            break

    # Enemy movement
    for enemy in enemies:
        if enemy[0] < block_x:
            enemy[0] += ENEMY_SPEED
        elif enemy[0] > block_x:
            enemy[0] -= ENEMY_SPEED
        if enemy[1] < block_y:
            enemy[1] += ENEMY_SPEED
        elif enemy[1] > block_y:
            enemy[1] -= ENEMY_SPEED
        
        # Check collision with player
        enemy_rect = pygame.Rect(enemy[0] - block_x + SCREEN_WIDTH // 2, enemy[1] - block_y + SCREEN_HEIGHT // 2, ENEMY_SIZE, ENEMY_SIZE)
        if player_rect.colliderect(enemy_rect):
            health -= 1
            if health <= 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()

    # Drawing
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, SQUARE_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw blocks
    for block in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR, (block[0] - block_x + SCREEN_WIDTH // 2, block[1] - block_y + SCREEN_HEIGHT // 2, BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy[0] - block_x + SCREEN_WIDTH // 2, enemy[1] - block_y + SCREEN_HEIGHT // 2, ENEMY_SIZE, ENEMY_SIZE))
    
    # Draw health bar
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(screen, (0, 255, 0), (20, 20, HEALTH_BAR_WIDTH * (health / MAX_HEALTH), HEALTH_BAR_HEIGHT))
    
    pygame.display.flip()
    clock.tick(60)
