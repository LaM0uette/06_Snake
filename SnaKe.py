import curses
import datetime
import os
from random import randint
import json


letter_player = "#"
letter_food = "O"

with open(r"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\users.json") as file:
    data = json.load(file)
    user = data.get(str(os.getenv("USERNAME")))

def display_food(window, *args):
    window.addch(args[0], args[1], args[2])

def update_leaderboard(score):
    leaderboard_file = r"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\leaderboard\leaderboard.json"

    with open(leaderboard_file) as file:
        data = json.load(file)
        best_score = data.get(user)

    if score <= best_score: return

    with open(leaderboard_file, "r+", encoding="utf-8") as fichier:
        data = json.load(fichier)
        data.update({user: score})
        fichier.seek(0)
        json.dump(data, fichier, indent=4, ensure_ascii=False)
        fichier.truncate()

def end_game(score):
    score_fin = "\nScore: " + str(score)
    print(score_fin)

    with open(fr"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\logs\Logs_{user}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log", "w") as f:
        f.write(f"{user}\n{score_fin}")

    update_leaderboard(score)

def NewGame(h, w):
    curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    curses.resize_term(h, w)

    window = curses.newwin(h, w, 0, 0)
    window.keypad(True)  # Enable keypad
    window.nodelay(True)  # Makes it possible to not wait for the user input

    # Initiate values
    key = curses.KEY_RIGHT
    score = 0

    # Initialize first food and snake coordinates
    snake = [[1, 3], [1, 2], [1, 1]]
    food = [round(h/2), round(w/2)]

    # Display the first food
    display_food(window, food[0], food[1], letter_food)

    while key != 27:  # While they Esc key is not pressed
        window.border('|', '|', '-', '-', '+', '+', '+', '+')

        # Display the score and title
        window.addstr(0, 2, f'Score: {str(score)} ')
        window.addstr(0, round(w/2), ' SNAKE! ')

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

            display_food(window, food[0], food[1], letter_food)
        else:
            last = snake.pop()
            display_food(window, last[0], last[1], ' ')
        display_food(window, snake[0][0], snake[0][1], letter_player)

    curses.endwin()
    end_game(score)


run = True
while run:
    txt = input("Une partie ? (o|n) (c pour custom) : ")

    if txt.lower() == "o":
        NewGame(h=30, w=60)
    elif txt.lower() == "n":
        run = False
    elif txt.lower() == "c":
        size = int(input("Taille du terrain (10 Minimum) : "))
        NewGame(h=size, w=size*2)
    else:
        print("Saisie incorect !")
