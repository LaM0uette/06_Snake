import curses
import os
from random import randint


curses.initscr()  # Init
curses.noecho()  # Echo OFF
curses.curs_set(0)

window = curses.newwin(30, 60, 0, 0)  # Create new window H=30, W=60
curses.resize_term(30, 60)
window.keypad(True)  # Enable keypad
window.nodelay(True)  # Makes it possible to not wait for the user input


# Initiate values
key = curses.KEY_RIGHT
score = 0

# Initialize first food and snake coordinates
snake = [[5, 8], [5, 7], [5, 6]]
food = [10, 25]

# Display the first food
window.addch(food[0], food[1], 'O')

while key != 27:  # While they Esc key is not pressed

    window.border(0)

    # Display the score and title
    window.addstr(0, 2, f'Score: {str(score)} ')
    window.addstr(0, 27, ' SNAKE! ')

    # Make the snake faster as it eats more
    window.timeout(round(140 - (len(snake) / 5 + len(snake) / 10) % 120))

    event = window.getch()  # Refreshes the screen and then waits for the user to hit a key
    key = key if event == -1 else event

    # Calculates the new coordinates of the head of the snake.
    snake.insert(0, [snake[0][0] + (key == curses.KEY_DOWN and 1) + (key == curses.KEY_UP and -1), snake[0][1] + (key == curses.KEY_LEFT and -1) + (key == curses.KEY_RIGHT and 1)])

    # Exit if snake crosses the boundaries
    if snake[0][0] == 0 or snake[0][0] == 29 or snake[0][1] == 0 or snake[0][1] == 59: break

    #Exit if snake runs over itself
    if snake[0] in snake[1:]: break

    # When snake eats the food
    if snake[0] == food:
        food = []
        score += 1
        while not food:

            # Generate coordinates for next food
            food = [randint(1, 28), randint(1, 58)]

            if food in snake: food = []

        window.addch(food[0], food[1], 'O')  #display the food
    else:
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], '#')

curses.endwin()  # Close the window and end the game
print("\nScore: " + str(score))
