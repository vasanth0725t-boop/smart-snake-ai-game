import pygame
import random
from collections import deque

pygame.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------
WIDTH = 800
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human vs AI - Smart Snake")

clock = pygame.time.Clock()

ROWS = HEIGHT // CELL
COLS = WIDTH // CELL

# -----------------------------
# COLORS
# -----------------------------
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (50, 220, 80)
DARK_GREEN = (20, 130, 50)
BLUE = (50, 150, 255)
DARK_BLUE = (30, 80, 160)
RED = (240, 50, 50)
YELLOW = (255, 220, 50)

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 45)


# -----------------------------
# CREATE FOOD
# -----------------------------
def create_food(human, ai):
    while True:
        food = (
            random.randint(0, COLS - 1),
            random.randint(0, ROWS - 1)
        )

        if food not in human and food not in ai:
            return food


# -----------------------------
# BFS AI PATHFINDING
# -----------------------------
def find_path(start, goal, obstacles):

    queue = deque([start])
    visited = {start}
    parent = {}

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while queue:

        current = queue.popleft()

        if current == goal:

            path = []

            while current != start:
                path.append(current)
                current = parent[current]

            path.reverse()

            return path

        for dx, dy in directions:

            next_position = (
                current[0] + dx,
                current[1] + dy
            )

            # Stay inside screen
            if not (
                0 <= next_position[0] < COLS
                and 0 <= next_position[1] < ROWS
            ):
                continue

            # Avoid obstacles
            if next_position in obstacles:
                continue

            if next_position not in visited:

                visited.add(next_position)
                parent[next_position] = current
                queue.append(next_position)

    return []


# -----------------------------
# RESET GAME
# -----------------------------
def reset_game():

    human = [
        (8, 10),
        (7, 10),
        (6, 10)
    ]

    ai = [
        (31, 20),
        (30, 20),
        (29, 20)
    ]

    human_score = 0
    ai_score = 0

    food = create_food(human, ai)

    return human, ai, food, human_score, ai_score


# -----------------------------
# DRAW SNAKE
# -----------------------------
def draw_snake(snake, head_color, body_color):

    for i, segment in enumerate(snake):

        color = head_color if i == 0 else body_color

        pygame.draw.rect(
            screen,
            color,
            (
                segment[0] * CELL,
                segment[1] * CELL,
                CELL,
                CELL
            )
        )


# -----------------------------
# INITIAL GAME
# -----------------------------
human, ai, food, human_score, ai_score = reset_game()

human_direction = (1, 0)

running = True
game_over = False
winner = ""

move_timer = 0
AI_SPEED = 8

# -----------------------------
# MAIN LOOP
# -----------------------------
while running:

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Restart
            if event.key == pygame.K_r and game_over:

                human, ai, food, human_score, ai_score = reset_game()

                human_direction = (1, 0)

                game_over = False
                winner = ""

            # HUMAN CONTROLS
            if not game_over:

                if event.key == pygame.K_UP and human_direction != (0, 1):
                    human_direction = (0, -1)

                elif event.key == pygame.K_DOWN and human_direction != (0, -1):
                    human_direction = (0, 1)

                elif event.key == pygame.K_LEFT and human_direction != (1, 0):
                    human_direction = (-1, 0)

                elif event.key == pygame.K_RIGHT and human_direction != (-1, 0):
                    human_direction = (1, 0)

    if not game_over:

        move_timer += 1

        if move_timer >= AI_SPEED:

            move_timer = 0

            # ---------------------
            # HUMAN MOVEMENT
            # ---------------------
            human_head = human[0]

            new_human_head = (
                human_head[0] + human_direction[0],
                human_head[1] + human_direction[1]
            )

            # Human wall collision
            if not (
                0 <= new_human_head[0] < COLS
                and 0 <= new_human_head[1] < ROWS
            ):

                game_over = True
                winner = "AI WINS!"

            # Human body collision
            elif new_human_head in human:

                game_over = True
                winner = "AI WINS!"

            else:

                human.insert(0, new_human_head)

                if new_human_head == food:

                    human_score += 1

                else:

                    human.pop()

            # ---------------------
            # AI MOVEMENT
            # ---------------------
            if not game_over:

                ai_head = ai[0]

                obstacles = set(human[:-1] + ai[:-1])

                path = find_path(
                    ai_head,
                    food,
                    obstacles
                )

                if path:

                    new_ai_head = path[0]

                    ai.insert(0, new_ai_head)

                    if new_ai_head == food:

                        ai_score += 1

                    else:

                        ai.pop()

                else:

                    # AI cannot find a path
                    game_over = True
                    winner = "HUMAN WINS!"

            # ---------------------
            # FOOD
            # ---------------------
            if not game_over:

                if human[0] == food or ai[0] == food:

                    food = create_food(human, ai)

            # ---------------------
            # AI BODY COLLISION
            # ---------------------
            if not game_over:

                if len(ai) != len(set(ai)):

                    game_over = True
                    winner = "HUMAN WINS!"

            # ---------------------
            # HUMAN BODY COLLISION
            # ---------------------
            if not game_over:

                if len(human) != len(set(human)):

                    game_over = True
                    winner = "AI WINS!"

            # ---------------------
            # SNAKE VS SNAKE
            # ---------------------
            if not game_over:

                if human[0] in ai:

                    game_over = True
                    winner = "AI WINS!"

                elif ai[0] in human:

                    game_over = True
                    winner = "HUMAN WINS!"

            # ---------------------
            # SCORE WIN
            # ---------------------
            if human_score >= 10:

                game_over = True
                winner = "HUMAN WINS!"

            elif ai_score >= 10:

                game_over = True
                winner = "AI WINS!"

    # -------------------------
    # DRAW BACKGROUND
    # -------------------------
    screen.fill(BLACK)

    # Grid
    for x in range(0, WIDTH, CELL):

        pygame.draw.line(
            screen,
            (35, 35, 35),
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, CELL):

        pygame.draw.line(
            screen,
            (35, 35, 35),
            (0, y),
            (WIDTH, y)
        )

    # -------------------------
    # DRAW FOOD
    # -------------------------
    pygame.draw.rect(
        screen,
        RED,
        (
            food[0] * CELL,
            food[1] * CELL,
            CELL,
            CELL
        )
    )

    # -------------------------
    # DRAW HUMAN
    # -------------------------
    draw_snake(
        human,
        GREEN,
        DARK_GREEN
    )

    # -------------------------
    # DRAW AI
    # -------------------------
    draw_snake(
        ai,
        BLUE,
        DARK_BLUE
    )

    # -------------------------
    # INFORMATION
    # -------------------------
    human_text = font.render(
        f"HUMAN: {human_score}",
        True,
        GREEN
    )

    ai_text = font.render(
        f"AI: {ai_score}",
        True,
        BLUE
    )

    screen.blit(human_text, (20, 10))
    screen.blit(ai_text, (680, 10))

    instruction = font.render(
        "Arrow Keys = Human",
        True,
        WHITE
    )

    screen.blit(
        instruction,
        (300, 10)
    )

    # -------------------------
    # GAME OVER
    # -------------------------
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)
        overlay.fill(BLACK)

        screen.blit(overlay, (0, 0))

        winner_text = big_font.render(
            winner,
            True,
            YELLOW
        )

        screen.blit(
            winner_text,
            (
                WIDTH // 2 -
                winner_text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )

    pygame.display.flip()

    clock.tick(30)


pygame.quit()
