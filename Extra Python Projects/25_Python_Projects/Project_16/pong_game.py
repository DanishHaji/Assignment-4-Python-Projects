import turtle
import random
import time

# Set up the screen
win = turtle.Screen()
win.title("Pong Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Stops screen updates for better performance

# Score tracking
left_score = 0
right_score = 0

# Display scores
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Player A: {left_score}  Player B: {right_score}", align="center", font=("Courier", 24, "normal"))

# Paddle class
class Paddle(turtle.Turtle):
    def __init__(self, x_position: int):
        super().__init__()
        self.speed(0)  # No animation delay
        self.shape("square")  # Paddle shape
        self.color("white")  # Paddle color
        self.shapesize(stretch_wid=5, stretch_len=1)  # Stretch paddle
        self.penup()  # Prevent drawing on screen
        self.goto(x_position, 0)  # Paddle starting position

    def move_up(self):
        # Move the paddle up if it's within the screen boundary
        if self.ycor() < 250:
            self.sety(self.ycor() + 20)

    def move_down(self):
        # Move the paddle down if it's within the screen boundary
        if self.ycor() > -240:
            self.sety(self.ycor() - 20)

# Ball class
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)  # No animation delay
        self.shape("square")  # Ball shape
        self.color("white")  # Ball color
        self.penup()  # Prevent drawing on screen
        self.goto(0, 0)  # Ball starting position
        self.dx = random.choice([-2, 2])  # Randomize initial direction
        self.dy = random.choice([-2, 2])

    def move(self):
        # Move the ball based on its speed
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

        # Collision with top/bottom boundaries
        if self.ycor() > 290 or self.ycor() < -290:
            self.dy *= -1  # Reverse vertical direction

# Function to update scores
def update_score():
    score_display.clear()
    score_display.write(f"Player A: {left_score}  Player B: {right_score}", align="center", font=("Courier", 24, "normal"))

# Function to start or pause/resume the game
def toggle_pause():
    global game_paused
    game_paused = not game_paused

# Create paddles and ball
left_paddle = Paddle(-350)
right_paddle = Paddle(350)
ball = Ball()

# Keyboard bindings
win.listen()
win.onkeypress(left_paddle.move_up, "w")  # Left paddle moves up
win.onkeypress(left_paddle.move_down, "s")  # Left paddle moves down
win.onkeypress(right_paddle.move_up, "Up")  # Right paddle moves up
win.onkeypress(right_paddle.move_down, "Down")  # Right paddle moves down
win.onkeypress(toggle_pause, "space")  # Toggle pause/resume with spacebar

# Game loop
game_paused = True
while True:
    win.update()  # Update screen

    if game_paused:
        score_display.goto(0, 0)
        score_display.write("Press SPACE to Start or Pause!", align="center", font=("Courier", 24, "bold"))
        time.sleep(0.1)
        continue  # Skip rest of loop if paused

    ball.move()  # Move ball
    time.sleep(0.01)  # Add slight delay for better performance

    # Ball collision with paddles
    if (ball.xcor() > 340 and ball.xcor() < 350) and (right_paddle.ycor() - 50 < ball.ycor() < right_paddle.ycor() + 50):
        ball.setx(340)  # Prevent overlapping
        ball.dx *= -1
        ball.dx *= 1.1  # Increase speed by 10%
        ball.dy *= 1.1  # Increase speed by 10%

    if (ball.xcor() < -340 and ball.xcor() > -350) and (left_paddle.ycor() - 50 < ball.ycor() < left_paddle.ycor() + 50):
        ball.setx(-340)  # Prevent overlapping
        ball.dx *= -1
        ball.dx *= 1.1  # Increase speed by 10%
        ball.dy *= 1.1  # Increase speed by 10%

    # Ball out of bounds (reset and scoring)
    if ball.xcor() > 390:
        left_score += 1  # Increase left paddle's score
        ball.goto(0, 0)  # Reset ball position
        ball.dx = random.choice([-2, 2])  # Randomize initial direction
        ball.dy = random.choice([-2, 2])
        update_score()

    if ball.xcor() < -390:
        right_score += 1  # Increase right paddle's score
        ball.goto(0, 0)  # Reset ball position
        ball.dx = random.choice([-2, 2])  # Randomize initial direction
        ball.dy = random.choice([-2, 2])
        update_score()

    # Winning condition
    if left_score == 5:
        score_display.goto(0, 0)
        score_display.write("Player A Wins!", align="center", font=("Courier", 36, "bold"))
        break  # End game loop

    if right_score == 5:
        score_display.goto(0, 0)
        score_display.write("Player B Wins!", align="center", font=("Courier", 36, "bold"))
        break  # End game loop
