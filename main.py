import pygame

pygame.init()

# Configurations
WIDTH, HEIGHT = 1200, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
run = True

# Colors
BLUE = (0, 139, 139)
WHITE = (255, 255, 255)
ORANGE = (251, 140, 29)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont('Arial', 48)
small_font = pygame.font.SysFont('Arial', 32)

# Variables
player_1_name = "Jogador 1"
player_2_name = "Jogador 2"
game_started = False

def input_names():
    global player_1_name, player_2_name, game_started

    input_active_1 = input_active_2 = False
    player_1_name = ""
    player_2_name = ""

    input_box_1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 50)
    input_box_2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

    clock = pygame.time.Clock()
    while not game_started:
        wn.fill(BLUE)

        # Render input boxes
        pygame.draw.rect(wn, WHITE, input_box_1, 2)
        pygame.draw.rect(wn, WHITE, input_box_2, 2)
        pygame.draw.rect(wn, GREEN, start_button)

        # Text instructions
        instruction_text = small_font.render("Digite os nomes dos jogadores e clique em iniciar", True, WHITE)
        wn.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 150))

        # Input texts
        txt_surface_1 = small_font.render(player_1_name, True, WHITE)
        txt_surface_2 = small_font.render(player_2_name, True, WHITE)
        wn.blit(txt_surface_1, (input_box_1.x + 10, input_box_1.y + 10))
        wn.blit(txt_surface_2, (input_box_2.x + 10, input_box_2.y + 10))

        # Start button text
        start_text = small_font.render("Iniciar", True, BLUE)
        wn.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
                             start_button.y + (start_button.height - start_text.get_height()) // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_1.collidepoint(event.pos):
                    input_active_1 = True
                    input_active_2 = False
                elif input_box_2.collidepoint(event.pos):
                    input_active_1 = False
                    input_active_2 = True
                elif start_button.collidepoint(event.pos):
                    if player_1_name and player_2_name:
                        game_started = True

            elif event.type == pygame.KEYDOWN:
                if input_active_1:
                    if event.key == pygame.K_BACKSPACE:
                        player_1_name = player_1_name[:-1]
                    else:
                        player_1_name += event.unicode
                elif input_active_2:
                    if event.key == pygame.K_BACKSPACE:
                        player_2_name = player_2_name[:-1]
                    else:
                        player_2_name += event.unicode

        pygame.display.flip()
        clock.tick(30)

def main_game():
    global player_1_name, player_2_name, run

    # Ball
    radius = 15
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_vel_x, ball_vel_y = 5, 5

    # Paddles
    paddle_width, paddle_height = 20, 120
    left_paddle_y = right_paddle_y = HEIGHT // 2 - paddle_height // 2
    paddle_speed = 7

    # Scores
    player_1_score = 0
    player_2_score = 0
    winner = None

    clock = pygame.time.Clock()

    while run:
        wn.fill(BLUE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Check for a winner
        if player_1_score >= 3:
            winner = player_1_name
        elif player_2_score >= 3:
            winner = player_2_name

        if winner:
            # Display the winner
            winner_text = font.render(f"{winner} venceu!", True, GREEN)
            wn.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Pause for 3 seconds to show the winner
            break  # Exit the game loop

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_y > 0:
            left_paddle_y -= paddle_speed
        if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
            left_paddle_y += paddle_speed
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
            right_paddle_y += paddle_speed

        # Ball movement
        ball_x += ball_vel_x
        ball_y += ball_vel_y

        # Ball collision with walls
        if ball_y - radius <= 0 or ball_y + radius >= HEIGHT:
            ball_vel_y = -ball_vel_y

        # Ball collision with paddles
        if (left_paddle_y < ball_y < left_paddle_y + paddle_height and ball_x - radius <= 70) or \
           (right_paddle_y < ball_y < right_paddle_y + paddle_height and ball_x + radius >= WIDTH - 70):
            ball_vel_x = -ball_vel_x

        # Scoring
        if ball_x - radius <= 0:
            player_2_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        if ball_x + radius >= WIDTH:
            player_1_score += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2

        # Draw paddles, ball, and scores
        pygame.draw.rect(wn, ORANGE, (50, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(wn, ORANGE, (WIDTH - 70, right_paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(wn, WHITE, (int(ball_x), int(ball_y)), radius)

        score_text = font.render(f"{player_1_score} - {player_2_score}", True, WHITE)
        wn.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Player names
        name_1 = small_font.render(player_1_name, True, WHITE)
        name_2 = small_font.render(player_2_name, True, WHITE)
        wn.blit(name_1, (50, 20))
        wn.blit(name_2, (WIDTH - 50 - name_2.get_width(), 20))

        pygame.display.flip()
        clock.tick(60)

# Run the game
input_names()
main_game()
pygame.quit()
