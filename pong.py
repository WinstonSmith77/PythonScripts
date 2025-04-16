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

ball = None
ball_speed = None
consecutive_hits = 0



clock = pygame.time.Clock()

# Spiel-Loop
running = True
while running:
    dt = clock.tick(60)
    win.fill(WHITE)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player[0] -= PLAYER_SPEED

    if keys[pygame.K_RIGHT]:
        player[0] += PLAYER_SPEED

    if keys[pygame.K_SPACE]:
        ball = [float(player[0]), float(player[1])]
        random_x = (random() * 6) - 3
        ball_speed = [float(random_x), float(-8)]
        consecutive_hits = 0

    # movement ball
    if ball and ball_speed:
        ball[0] += ball_speed[0]
        ball[1] += ball_speed[1]

        # top
        if ball[1] < 0:
            ball[1] = -ball[1]
            ball_speed[1] = -ball_speed[1]

        # left
        if ball[0] < 0:
            ball[0] = -ball[0]
            ball_speed[0] = -ball_speed[0]

        # right
        if ball[0] > WIDTH:
            ball[0] = 2 * WIDTH - ball[0]
            ball_speed[0] = -ball_speed[0]

        # racket
        if ball[1] > HEIGHT - OFFSET_Y_IN_RACKET_HEIGHT * HEIGHT_RACKET:
            if ball[0] > player[0] - WIDTH_RACKET // 2 and ball[0] < player[0] + WIDTH_RACKET // 2:
                ball[1] = player[1] - HEIGHT_RACKET // 2
                ball[1] = -ball[1]
                ball_speed = [ball_speed[0] * 1.0, ball_speed[1] * 1.0]
                consecutive_hits += 1
            else:
                ball = ball_speed = None

    def render_rect(pos_center, width: int, height: int, color):
        rect = (pos_center[0] - width // 2, pos_center[1] - height //
                2, width, height)
        pygame.draw.rect(win,  color, rect)

    player[0] = min(WIDTH - WIDTH_RACKET, player[0])
    player[0] = max(WIDTH_RACKET, player[0])

    # current_image = get_frame(sprite_sheet, frame)
   # win.blit(current_image, player_pos)

    render_rect(player, WIDTH_RACKET, HEIGHT_RACKET, RED)

    if ball:
        render_rect(ball, HEIGHT_BALL, HEIGHT_BALL, BLUE)
bsNone
b_
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
