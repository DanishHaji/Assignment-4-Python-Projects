import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20  # Snake block size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Display score
def display_score(score):
    value = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

# Snake class
class Snake:
    def __init__(self):
        self.body = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = "UP"
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = [head_x, head_y]
        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()  # Remove tail unless growing
        else:
            self.growing = False  # Stop growing after one move

    def grow(self):
        self.growing = True  # Set flag to grow

    def check_collision(self):
        head = self.body[0]

        # Check collision with itself
        if head in self.body[1:]:
            return True
        
        # Check collision with walls
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True

        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

# Food class
class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if [x, y] not in snake.body:  # Ensure food doesn't spawn inside the snake
                return [x, y]

    def draw(self):
        pygame.draw.rect(screen, RED, [self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE])

# Main game loop
def game_loop():
    global snake, food
    snake = Snake()
    food = Food()

    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        # Check for collision with food
        if snake.body[0] == food.position:
            food.position = food.random_position()
            snake.grow()

        # Check for collision with itself or walls
        if snake.check_collision():
            running = False

        # Draw game elements
        snake.draw()
        food.draw()
        display_score(len(snake.body) - 1)
        pygame.display.update()

        # Control speed
        clock.tick(10)

    # Game Over Screen
    game_over()

# Game over function with restart option
def game_over():
    screen.fill(BLACK)
    message = font_style.render("Game Over! Press 'R' to Restart or 'Q' to Quit.", True, WHITE)
    screen.blit(message, [WIDTH // 6, HEIGHT // 3])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Start the game
game_loop()
