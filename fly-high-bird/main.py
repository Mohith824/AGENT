import math
import random
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fly High Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 20)

SKY = (110, 200, 245)
GROUND = (222, 178, 73)
GREEN = (64, 177, 76)
DARK_GREEN = (38, 132, 55)
WHITE = (255, 255, 255)


def new_pipe(x):
    gap = 175
    top_height = random.randint(100, 390)
    return {"x": x, "top": top_height, "gap": gap, "scored": False}


def reset():
    return {
        "bird_x": 120.0,
        "bird_y": HEIGHT / 2,
        "velocity": 0.0,
        "pipes": [new_pipe(520), new_pipe(790)],
        "score": 0,
        "started": False,
        "game_over": False,
    }


def draw_bird(x, y):
    x, y = int(x), int(y)
    pygame.draw.ellipse(screen, (250, 215, 55), (x - 18, y - 14, 38, 30))
    pygame.draw.ellipse(screen, (235, 178, 30), (x - 18, y - 2, 22, 13))
    pygame.draw.polygon(screen, (238, 105, 40), [(x + 17, y - 2), (x + 34, y + 4), (x + 17, y + 8)])
    pygame.draw.circle(screen, WHITE, (x + 9, y - 8), 7)
    pygame.draw.circle(screen, (30, 30, 30), (x + 11, y - 8), 3)


def draw_pipe(pipe):
    x = int(pipe["x"])
    top = pipe["top"]
    bottom_y = top + pipe["gap"]
    pygame.draw.rect(screen, GREEN, (x, 0, 70, top))
    pygame.draw.rect(screen, GREEN, (x, bottom_y, 70, HEIGHT - bottom_y - 70))
    pygame.draw.rect(screen, DARK_GREEN, (x, 0, 8, top))
    pygame.draw.rect(screen, DARK_GREEN, (x, bottom_y, 8, HEIGHT - bottom_y - 70))
    pygame.draw.rect(screen, GREEN, (x - 8, top - 25, 86, 25))
    pygame.draw.rect(screen, GREEN, (x - 8, bottom_y, 86, 25))


def draw_background():
    screen.fill(SKY)
    for cx, cy, size in [(90, 115, 1.0), (330, 180, .8), (220, 55, .65)]:
        pygame.draw.circle(screen, WHITE, (cx, cy), int(25 * size))
        pygame.draw.circle(screen, WHITE, (cx + 28, cy + 6), int(20 * size))
        pygame.draw.circle(screen, WHITE, (cx - 27, cy + 8), int(18 * size))
    pygame.draw.rect(screen, GROUND, (0, HEIGHT - 70, WIDTH, 70))
    for x in range(-20, WIDTH, 35):
        pygame.draw.line(screen, (196, 145, 46), (x, HEIGHT - 70), (x + 20, HEIGHT), 3)


def text_center(message, y, fnt=font, color=WHITE):
    image = fnt.render(message, True, color)
    screen.blit(image, (WIDTH // 2 - image.get_width() // 2, y))


def main():
    state = reset()
    running = True
    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if state["game_over"]:
                    state = reset()
                    state["started"] = True
                else:
                    state["started"] = True
                    state["velocity"] = -430
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state["game_over"]:
                    state = reset()
                    state["started"] = True
                else:
                    state["started"] = True
                    state["velocity"] = -430

        if state["started"] and not state["game_over"]:
            state["velocity"] += 1150 * dt
            state["bird_y"] += state["velocity"] * dt
            for pipe in state["pipes"]:
                pipe["x"] -= 190 * dt
                if not pipe["scored"] and pipe["x"] + 70 < state["bird_x"]:
                    pipe["scored"] = True
                    state["score"] += 1
            if state["pipes"][0]["x"] < -90:
                state["pipes"].pop(0)
                state["pipes"].append(new_pipe(state["pipes"][-1]["x"] + 270))

            bird_rect = pygame.Rect(int(state["bird_x"] - 15), int(state["bird_y"] - 12), 31, 25)
            if state["bird_y"] - 12 < 0 or state["bird_y"] + 12 > HEIGHT - 70:
                state["game_over"] = True
            for pipe in state["pipes"]:
                top_rect = pygame.Rect(int(pipe["x"]), 0, 70, pipe["top"])
                bottom_rect = pygame.Rect(int(pipe["x"]), pipe["top"] + pipe["gap"], 70, HEIGHT)
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    state["game_over"] = True

        draw_background()
        for pipe in state["pipes"]:
            draw_pipe(pipe)
        draw_bird(state["bird_x"], state["bird_y"])
        score_img = font.render(str(state["score"]), True, WHITE)
        screen.blit(score_img, (WIDTH // 2 - score_img.get_width() // 2, 25))

        if not state["started"]:
            text_center("FLY HIGH BIRD", 250)
            text_center("Press SPACE or click to flap", 300, small_font)
        elif state["game_over"]:
            pygame.draw.rect(screen, (20, 70, 100), (65, 245, WIDTH - 130, 150), border_radius=14)
            text_center("GAME OVER", 265)
            text_center(f"Score: {state['score']}", 310, small_font)
            text_center("Press SPACE to try again", 345, small_font)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
