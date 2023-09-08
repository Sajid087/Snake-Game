import tkinter as tk
import random
import time

# Constants
WIDTH, HEIGHT = 400, 400
SNAKE_SIZE = 20
MOVE_DELAY = 100
SPEED_MULTIPLIER = 0.9  # Speed increase factor on each level

# Initialize variables
snake = [(100, 50), (90, 50), (80, 50)]
snake_direction = 'Right'
food_position = (200, 200)
score = 0
level = 1
speed = MOVE_DELAY

# High score
try:
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Functions
def create_food():
    global food_position
    while True:
        x = random.randint(1, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(1, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_position = (x, y)
        if food_position not in snake:
            break
    canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill='red')

def move_snake():
    global snake_direction, score, level, speed, high_score

    # Calculate the new head position
    head_x, head_y = snake[0]
    if snake_direction == 'Up':
        head_y -= SNAKE_SIZE
    elif snake_direction == 'Down':
        head_y += SNAKE_SIZE
    elif snake_direction == 'Left':
        head_x -= SNAKE_SIZE
    elif snake_direction == 'Right':
        head_x += SNAKE_SIZE

    # Check if the snake has eaten the food
    if (head_x, head_y) == food_position:
        score += 1
        if score > high_score:
            high_score = score
            with open('high_score.txt', 'w') as file:
                file.write(str(high_score))
        if score % 5 == 0:
            level += 1
            speed = int(speed * SPEED_MULTIPLIER)
            canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                text=f'Level {level}',
                font=('Helvetica', 20)
            )
            canvas.update()
            time.sleep(1)
        create_food()
    else:
        # Remove the tail of the snake
        tail_x, tail_y = snake.pop()
        canvas.delete(canvas.find_closest(tail_x + SNAKE_SIZE / 2, tail_y + SNAKE_SIZE / 2))
        
    # Check if the snake collided with itself or the wall
    if (
        (head_x < 0)
        or (head_x >= WIDTH)
        or (head_y < 0)
        or (head_y >= HEIGHT)
        or ((head_x, head_y) in snake)
    ):
        game_over()
        return

    # Add the new head to the snake
    snake.insert(0, (head_x, head_y))
    canvas.create_rectangle(head_x, head_y, head_x + SNAKE_SIZE, head_y + SNAKE_SIZE, fill='green')

    # Update the score and speed label
    score_label.config(text=f'Score: {score} | Level: {level} | High Score: {high_score}')
    speed_label.config(text=f'Speed: {speed} ms')

    # Set a timer to move the snake again
    root.after(speed, move_snake)

def game_over():
    canvas.create_text(
        WIDTH // 2, HEIGHT // 2,
        text=f'Game Over! Your Score: {score}',
        font=('Helvetica', 20)
    )
    root.quit()

def change_direction(new_direction):
    global snake_direction
    opposite_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
    if new_direction != opposite_directions.get(snake_direction):
        snake_direction = new_direction

# Create the main window
root = tk.Tk()
root.title('Snake Game')

# Create the canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Create the score label
score_label = tk.Label(root, text=f'Score: {score} | Level: {level} | High Score: {high_score}', font=('Helvetica', 12))
score_label.pack()

# Create the speed label
speed_label = tk.Label(root, text=f'Speed: {speed} ms', font=('Helvetica', 12))
speed_label.pack()

# Bind arrow keys to change snake direction
root.bind('<Up>', lambda event: change_direction('Up'))
root.bind('<Down>', lambda event: change_direction('Down'))
root.bind('<Left>', lambda event: change_direction('Left'))
root.bind('<Right>', lambda event: change_direction('Right'))

# Create the initial snake and food
for segment in snake:
    x, y = segment
    canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill='green')
create_food()

# Start the game loop
root.after(speed, move_snake)

# Run the main loop
root.mainloop()
 