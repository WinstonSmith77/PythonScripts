import pygame
import sys
from random import random

# Initialisierung
pygame.init()
WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("Pong")

WIDTH_RACKET = 70
HEIGHT_RACKET = 10
HEIGHT_BALL = 10
PLAYER_SPEED = 4
OFFSET_Y_IN_RACKET_HEIGHT = 3

# Farben
WHITE = (255, 255, 255)
RED = (255, 56, 12)
BLUE = (150, 77, 80)
GREEN = (60, 200, 199)
# Spielfigur

player = [WIDTH // 2, HEIGHT - OFFSET_Y_IN_RACKET_HEIGHT * HEIGHT_RACKET]


class Ball:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

balls = []



clock = pygame.time.Clock()

# Spiel-Loop
running = True
space_was_pressed = False
consecutive_hits = 0
while running:
    dt = clock.tick(30)
    win.fill(WHITE)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player[0] -= PLAYER_SPEED

    if keys[pygame.K_RIGHT]:
        player[0] += PLAYER_SPEED

    if keys[pygame.K_SPACE]:
        if not space_was_pressed:
            random_x = (random() * 6) - 3
            #balls.clear()
            balls.append(Ball([float(player[0]), float(player[1])],  [float(random_x), float(-8)]))
            space_was_pressed = True
    else:
        space_was_pressed = False

    def check_ball_collision(ball : Ball, player) -> tuple[bool, int]: 
        consecutive_hits = 0
        ball.position[0] += ball.speed[0]
        ball.position[1] += ball.speed[1]

        # top
        if ball.position[1] < 0:
            ball.position[1] = -ball.position[1]
            ball.speed[1] = -ball.speed[1]

        # left
        if ball.position[0] < 0:
            ball.position[0] = -ball.position[0]
            ball.speed[0] = -ball.speed[0]

        # right
        if ball.position[0] > WIDTH:
            ball.position[0] = 2 * WIDTH - ball.position[0]
            ball.speed[0] = -ball.speed[0]

        # racket
        if ball.position[1] > HEIGHT - OFFSET_Y_IN_RACKET_HEIGHT * HEIGHT_RACKET:
            if ball.position[0] > player[0] - WIDTH_RACKET // 2 and ball.position[0] < player[0] + WIDTH_RACKET // 2:
                ball.position[1] = player[1] - HEIGHT_RACKET // 2
                ball.position[1] = -ball.position[1]
                ball.speed = [ball.speed[0] * 1.0, ball.speed[1] * 1.0]
                consecutive_hits += 1
        
        #bottom
        if ball.position[1] > HEIGHT:
            return (True, consecutive_hits)    

        return (False, consecutive_hits)    

      
    # movement ball
    if balls:
        for ball in balls:
           result = check_ball_collision(ball, player)
           if result[0]:
                balls.remove(ball)
           consecutive_hits += result[1]   

    def render_rect(pos_center, width: int, height: int, color):
        rect = (pos_center[0] - width // 2, pos_center[1] - height //
                2, width, height)
        pygame.draw.rect(win,  color, rect)

    player[0] = min(WIDTH - WIDTH_RACKET, player[0])
    player[0] = max(WIDTH_RACKET, player[0])

    # current_image = get_frame(sprite_sheet, frame)
   # win.blit(current_image, player_pos)

    render_rect(player, WIDTH_RACKET, HEIGHT_RACKET, RED)

    for ball in balls:
        render_rect(ball.position, HEIGHT_BALL, HEIGHT_BALL, BLUE)

    # font = pygame.font.SysFont('Comic Sans MS', 30)
    # text_surface = font.render(
    #     str(player[0]) + " " + str(ball) + " " + str(ball_speed), False, (0, 0, 0))
    # win.blit(text_surface, (0, 0))

    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(
        str(consecutive_hits), False, (0, 0, 0))
    win.blit(text_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
