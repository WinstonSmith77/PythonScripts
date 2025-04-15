import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen size and colors
WIDTH = 1200
HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WASD Movement")

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

shot_size = 5

# Clock to control frame rate
clock = pygame.time.Clock()


shots = []
shot_speed = 10

# Main game loop
running = True
while running:
    fireShot = False
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # WASD movement logic
    if keys[pygame.K_w]:  # Move up
        player_y -= player_speed
    if keys[pygame.K_s]:  # Move down
        player_y += player_speed
    if keys[pygame.K_a]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]:  # Move right
        player_x += player_speed

    if keys[pygame.K_SPACE]:  # Move right
        fireShot = True

    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    if fireShot:
        shots.append((player_x + player_size // 2, player_y + player_size // 2))

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))

    shots = [(shot[0], shot[1] - shot_speed) for shot in shots if shot[1] > shot_speed]
   

    for shot in shots:
        pygame.draw.rect(screen, (0, 0, 255), (shot[0] - 5, shot[1] -5 , 5, 5))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
