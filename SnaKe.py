import curses
import os
from random import randint


curses.initscr()
curses.noecho()
curses.curs_set(0)
letter_player = "#"
letter_food = "O"

def NewGame(h, w):
    curses.resize_term(h, w)
    window = curses.newwin(h, w, 0, 0)
    window.keypad(True)  # Enable keypad
    window.nodelay(True)  # Makes it possible to not wait for the user input

    # Initiate values
    key = curses.KEY_RIGHT
    score = 0

    # Initialize first food and snake coordinates
    snake = [[5, 8], [5, 7], [5, 6]]
    food = [10, 25]

    # Display the first food
    window.addch(food[0], food[1], letter_food)

    while key != 27:  # While they Esc key is not pressed
        window.border('|', '|', '-', '-', '+', '+', '+', '+')

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
        if snake[0][0] == 0 or snake[0][0] == h-1 or snake[0][1] == 0 or snake[0][1] == w-1: break

        #Exit if snake runs over itself
        if snake[0] in snake[1:]: break

        # When snake eats the food
        if snake[0] == food:
            food = []
            score += 1
            while not food:

                # Generate coordinates for next food
                food = [randint(1, h-2), randint(1, w-2)]

                if food in snake: food = []

            window.addch(food[0], food[1], letter_food)  #display the food
        else:
            last = snake.pop()
            window.addch(last[0], last[1], ' ')
        window.addch(snake[0][0], snake[0][1], letter_player)

    curses.endwin()
    print("\nScore: " + str(score))


NewGame(h=30, w=60)

os.system("pause > nul")
