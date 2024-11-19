import pygame
import random

pygame.init()

# Configurations
WIDTH, HEIGHT = 1000, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
run = True
player_1 = player_2 = 0
direction = [0, 1]
angle = [0, 1, 2]

# Colors
BLUE = (0, 139, 139)
WHITE = (255, 255, 255)

# Ball
radius = 15
ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
ball_vel_x, ball_vel_y = 1.2, 1.2

# Players
paddle_width, paddle_height = 20, 120
left_paddle_y = right_paddle_y = HEIGHT/2 - paddle_height/2
left_paddle_x, right_paddle_x = 50, WIDTH - 70
right_paddle_vel = left_paddle_vel = 0

# Fonts
font = pygame.font.SysFont('Arial', 48)
small_font = pygame.font.SysFont('Arial', 32)

while run:
    wn.fill(BLUE)

    pygame.draw.line(wn, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)
    pygame.draw.rect(wn, WHITE, (10, 10, WIDTH - 20, HEIGHT - 20), 5)

    player_1_text = small_font.render("Jogador 1", True, WHITE)
    player_2_text = small_font.render("Jogador 2", True, WHITE)
    wn.blit(player_1_text, (20, 20))
    wn.blit(player_2_text, (WIDTH - player_2_text.get_width() - 20, 20))

    # Controls
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                right_paddle_vel = -0.9
            if i.key == pygame.K_DOWN:
                right_paddle_vel = 0.9
            if i.key == pygame.K_w:
                left_paddle_vel = -0.9
            if i.key == pygame.K_s:
                left_paddle_vel = 0.9

        if i.type == pygame.KEYUP:
            right_paddle_vel = 0
            left_paddle_vel = 0

    left_paddle_y += left_paddle_vel
    right_paddle_y += right_paddle_vel

    left_paddle_y = max(0, min(HEIGHT - paddle_height, left_paddle_y))
    right_paddle_y = max(0, min(HEIGHT - paddle_height, right_paddle_y))

    pygame.draw.rect(wn, WHITE, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, WHITE, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))

    ball_x += ball_vel_x
    ball_y += ball_vel_y

    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius:
        ball_vel_y *= -1

    if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
            ball_vel_x *= -1

    if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
            ball_vel_x *= -1

    # Points
    if ball_x >= WIDTH - radius:
        player_1 += 1
        ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
        ball_vel_x *= -1

    if ball_x <= 0 + radius:
        player_2 += 1
        ball_x, ball_y = WIDTH/2 - radius, HEIGHT/2 - radius
        ball_vel_x *= -1

    # Draw ball
    pygame.draw.circle(wn, WHITE, (int(ball_x), int(ball_y)), radius)

    # Score
    score_text = font.render(f"{player_1} - {player_2}", True, WHITE)
    wn.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    # Update view
    pygame.display.flip()
    pygame.time.delay(5)

pygame.quit()
