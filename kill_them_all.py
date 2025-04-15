import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("090285_metal-ping-1wav-86972.mp3")  # Replace with your file path

# Screen size and colors
WIDTH = 1200
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

#shots
shots = []
shot_speed = 10

# Font setup
font = pygame.font.Font(None, 74)  # Default font, size 74



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
    if keys[pygame.K_w] or keys[pygame.K_UP]:  # Move up
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Move down
        player_y += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
        player_x -= player_speed
    if keys[pygame.K_d]  or keys[pygame.K_RIGHT]:  # Move right
        player_x += player_speed

    if keys[pygame.K_SPACE]:  # Move right
        fireShot = True

    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    if fireShot:
        shots.append((player_x + player_size // 2, player_y + player_size // 2))
        sound.play()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))
    text = font.render(f"Shots live = {len(shots)}", True, BLACK, None)  # Text, anti-aliased, 
    screen.blit(text, (WIDTH - text.get_width() , 0))

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
