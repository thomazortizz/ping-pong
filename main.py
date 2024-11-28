import pygame
import time

pygame.init()

# Configurations
WIDTH, HEIGHT = 1200, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
run = True

# Colors
ORANGE = (255, 153, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_ORANGE = (173, 216, 230)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (3, 27, 52)  # #031B34

# Fonts
font = pygame.font.SysFont('Arial', 48)
small_font = pygame.font.SysFont('Arial', 32)

# Variables
player_1_name = "Jogador 1"
player_2_name = "Jogador 2"
game_started = False

# Load images
beer_image = pygame.image.load("img/beer.webp")
beer_image = pygame.transform.scale(beer_image, (100, 100))

background_image = pygame.image.load("img/background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def input_names():
    global player_1_name, player_2_name, game_started

    input_active_1 = input_active_2 = False
    player_1_name = ""
    player_2_name = ""

    input_box_1 = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 25, 200, 50)
    input_box_2 = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 - 25, 200, 50)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

    clock = pygame.time.Clock()
    cursor_visible = True
    last_blink = time.time()

    while not game_started:
        wn.blit(background_image, (0, 0)) 

        # Render input boxes
        pygame.draw.rect(wn, LIGHT_ORANGE if input_active_1 else DARK_GRAY, input_box_1, 0, border_radius=10)
        pygame.draw.rect(wn, LIGHT_ORANGE if input_active_2 else DARK_GRAY, input_box_2, 0, border_radius=10)
        pygame.draw.rect(wn, BUTTON_COLOR, start_button, 0, border_radius=10)

        # Render outlines for input boxes
        pygame.draw.rect(wn, WHITE, input_box_1, 2, border_radius=10)
        pygame.draw.rect(wn, WHITE, input_box_2, 2, border_radius=10)

        # Text instructions
        instruction_text = small_font.render("Digite os nomes dos jogadores e clique em iniciar", True, WHITE)
        wn.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 150))

        # Input texts
        txt_surface_1 = small_font.render(player_1_name or "Jogador 1", True, GRAY if not player_1_name else WHITE)
        txt_surface_2 = small_font.render(player_2_name or "Jogador 2", True, GRAY if not player_2_name else WHITE)
        wn.blit(txt_surface_1, (input_box_1.x + 10, input_box_1.y + 10))
        wn.blit(txt_surface_2, (input_box_2.x + 10, input_box_2.y + 10))

        # Draw blinking cursor for active inputs
        if input_active_1 and cursor_visible:
            cursor_x = input_box_1.x + 10 + txt_surface_1.get_width() + 5
            cursor_y = input_box_1.y + 10
            pygame.draw.rect(wn, WHITE, (cursor_x, cursor_y, 2, txt_surface_1.get_height()))
        if input_active_2 and cursor_visible:
            cursor_x = input_box_2.x + 10 + txt_surface_2.get_width() + 5
            cursor_y = input_box_2.y + 10
            pygame.draw.rect(wn, WHITE, (cursor_x, cursor_y, 2, txt_surface_2.get_height()))

        # Draw "X" between inputs
        x_text = font.render("X", True, WHITE)
        wn.blit(x_text, (WIDTH // 2 - x_text.get_width() // 2, HEIGHT // 2 - x_text.get_height() // 2))

        # Start button text
        start_text = small_font.render("Iniciar", True, WHITE)
        wn.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2,
                             start_button.y + (start_button.height - start_text.get_height()) // 2))

        # Blink logic for the cursor
        if time.time() - last_blink > 0.5:
            cursor_visible = not cursor_visible
            last_blink = time.time()

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
                    if player_1_name.strip() and player_2_name.strip():
                        game_started = True

            elif event.type == pygame.KEYDOWN:
                if input_active_1:
                    if event.key == pygame.K_BACKSPACE:
                        player_1_name = player_1_name[:-1]
                    elif len(player_1_name) < 20:  # Limit name length
                        player_1_name += event.unicode
                elif input_active_2:
                    if event.key == pygame.K_BACKSPACE:
                        player_2_name = player_2_name[:-1]
                    elif len(player_2_name) < 20:  # Limit name length
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
        wn.blit(background_image, (0, 0)) 

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
            loser = player_1_name if winner == player_2_name else player_2_name
            loser_text = font.render(f"{loser} bebe!", True, GREEN)
            wn.blit(loser_text, (WIDTH // 2 - loser_text.get_width() // 2, HEIGHT // 2 - loser_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

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

        # Draw beer image for goals
        wn.blit(beer_image, (25, left_paddle_y))  # Left goal
        wn.blit(beer_image, (WIDTH - 125, right_paddle_y))  # Right goal
        pygame.draw.circle(wn, WHITE, (ball_x, ball_y), radius)
        
        # Display scores
        score_1 = font.render(str(player_1_score), True, WHITE)
        score_2 = font.render(str(player_2_score), True, WHITE)
        wn.blit(score_1, (WIDTH // 4, 20))
        wn.blit(score_2, (3 * WIDTH // 4 - score_2.get_width(), 20))

        # Display player names
        name_1 = small_font.render(player_1_name, True, WHITE)
        name_2 = small_font.render(player_2_name, True, WHITE)
        wn.blit(name_1, (50, 20))
        wn.blit(name_2, (WIDTH - name_2.get_width() - 50, 20))

        pygame.display.flip()
        clock.tick(60)


# Main program flow
input_names()
main_game()
pygame.quit()
