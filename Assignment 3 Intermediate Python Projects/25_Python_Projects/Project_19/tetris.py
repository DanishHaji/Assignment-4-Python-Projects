import pygame
import random
import sys

pygame.init()

# Game Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        return [list(row) for row in zip(*self.shape[::-1])]

grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
score = 0

def is_valid_position(tetromino, x_offset=0, y_offset=0, new_shape=None):
    shape = new_shape if new_shape else tetromino.shape
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + x + x_offset
                new_y = tetromino.y + y + y_offset
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                    return False
    return True

def place_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines():
    global grid, score
    new_grid = [row for row in grid if BLACK in row]
    cleared_lines = ROWS - len(new_grid)
    grid = [[BLACK] * COLUMNS for _ in range(cleared_lines)] + new_grid
    score += cleared_lines * 100

def draw_screen(screen, tetromino):
    screen.fill(BLACK)

    # Draw grid
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw falling tetromino
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color, 
                                 ((tetromino.x + x) * BLOCK_SIZE, 
                                  (tetromino.y + y) * BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, WHITE, 
                                 ((tetromino.x + x) * BLOCK_SIZE, 
                                  (tetromino.y + y) * BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw score
    font = pygame.font.SysFont("monospace", 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

def game_loop():
    global score
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    tetromino = Tetromino()
    fall_time = 0
    fall_speed = 500
    game_over = False
    paused = False

    while not game_over:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick(30)

        if paused:
            font = pygame.font.SysFont("monospace", 50)
            text = font.render("Paused", True, WHITE)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            continue

        if fall_time > fall_speed:
            if is_valid_position(tetromino, y_offset=1):
                tetromino.y += 1
            else:
                place_tetromino(tetromino)
                clear_lines()
                tetromino = Tetromino()
                if not is_valid_position(tetromino):
                    game_over = True
            fall_time = 0
            fall_speed = max(100, fall_speed - 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_valid_position(tetromino, x_offset=-1):
                    tetromino.x -= 1
                if event.key == pygame.K_RIGHT and is_valid_position(tetromino, x_offset=1):
                    tetromino.x += 1
                if event.key == pygame.K_DOWN and is_valid_position(tetromino, y_offset=1):
                    tetromino.y += 1
                if event.key == pygame.K_UP:
                    rotated_shape = tetromino.rotate()
                    if is_valid_position(tetromino, new_shape=rotated_shape):
                        tetromino.shape = rotated_shape
                if event.key == pygame.K_p:  # Pause toggle
                    paused = not paused

        draw_screen(screen, tetromino)

    # Game Over screen
    font = pygame.font.SysFont("monospace", 50)
    text = font.render("Game Over!", True, WHITE)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Start the game
game_loop()
