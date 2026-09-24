import random
import sys

import pygame

# Window and grid settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 6

# Colors
BACKGROUND = (20, 20, 20)
GRID_COLOR = (35, 35, 35)
SNAKE_COLOR = (70, 200, 90)
HEAD_COLOR = (45, 160, 65)
FOOD_COLOR = (220, 70, 70)
TEXT_COLOR = (240, 240, 240)


def random_food(snake):
    available = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]
    return random.choice(available) if available else None


def draw_cell(screen, position, color, inset=1):
    x, y = position
    rectangle = pygame.Rect(
        x * CELL_SIZE + inset,
        y * CELL_SIZE + inset,
        CELL_SIZE - inset * 2,
        CELL_SIZE - inset * 2,
    )
    pygame.draw.rect(screen, color, rectangle, border_radius=4)


def draw_game(screen, snake, food, score, font):
    screen.fill(BACKGROUND)

    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

    for index, segment in enumerate(snake):
        draw_cell(screen, segment, HEAD_COLOR if index == 0 else SNAKE_COLOR)

    if food is not None:
        draw_cell(screen, food, FOOD_COLOR, inset=2)

    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 8))
    pygame.display.flip()


def game_over_screen(screen, score, title_font, font):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 175))
    screen.blit(overlay, (0, 0))

    title = title_font.render("Game Over", True, TEXT_COLOR)
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    instruction = font.render("Press R to restart or Q to quit", True, TEXT_COLOR)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 55)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(instruction, instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 45)))
    pygame.display.flip()


def run_game():
    pygame.init()
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    title_font = pygame.font.Font(None, 58)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    next_direction = direction
    food = random_food(snake)
    score = 0
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_direction = (1, 0)
                elif game_over and event.key == pygame.K_r:
                    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                    direction = (1, 0)
                    next_direction = direction
                    food = random_food(snake)
                    score = 0
                    game_over = False
                elif game_over and event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
            will_eat = new_head == food
            hit_body = new_head in (snake if will_eat else snake[:-1])

            if hit_wall or hit_body:
                game_over = True
            else:
                snake.insert(0, new_head)
                if will_eat:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        draw_game(screen, snake, food, score, font)
        if game_over:
            game_over_screen(screen, score, title_font, font)
            clock.tick(30)
        else:
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
