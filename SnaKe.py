import curses
import datetime
import os
from random import randint
import json

GUID = str(os.getenv("USERNAME"))
JSON_USERS = r"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\users.json"
LEADERBOARD = r"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\leaderboard"

class SnaKe:
    def __init__(self, h, w):
        self.letter_player = "#"
        self.letter_food = "O"
        self.height = h
        self.width = w
        self.user = None
        self.score = 0

        self.init_player()

    def open_json(self, file):
        with open(file) as js:
            return json.load(js)

    def update_json(self, file, dct):
        with open(file, "r+", encoding="utf-8") as fichier:
            data = json.load(fichier)
            data.update(dct)
            fichier.seek(0)
            json.dump(data, fichier, indent=4, ensure_ascii=False)
            fichier.truncate()

    def init_player(self):
        data = self.open_json(JSON_USERS)
        self.user = data.get(GUID)

        if self.user:
            self.update_json(JSON_USERS, {GUID: "Inconnu"})

    def write_log(self, file, score_fin):
        with open(file, "w") as js:
            js.write(f"{self.user}\n{score_fin}")

    def update_leaderboard(self):
        ldb = f"{LEADERBOARD}\leaderboard_{self.height}_{self.width}.json"

        data = self.open_json(ldb)
        best_score = data.get(self.user)

        if self.score <= best_score: return

        self.update_json(ldb, {self.user: self.score})

    def end_game(self):
        score_fin = "\nScore: " + str(self.score)

        self.write_log(fr"T:\- 4 Suivi Appuis\18-Partage\de VILLELE DORIAN\00_MINI_JEUX\SnaKe\logs\Logs_{self.user}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log", score_fin)

        print(score_fin)

        self.update_leaderboard()

    def display_food(self, window, *args):
        window.addch(args[0], args[1], args[2])

    def NewGame(self):
        curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        curses.resize_term(self.height, self.width)

        window = curses.newwin(self.height, self.width, 0, 0)
        window.keypad(True)  # Enable keypad
        window.nodelay(True)  # Makes it possible to not wait for the user input

        # Initiate values
        key = curses.KEY_RIGHT

        # Initialize first food and snake coordinates
        snake = [[1, 3], [1, 2], [1, 1]]
        food = [round(self.height / 2), round(self.width / 2)]

        # Display the first food
        self.display_food(window, food[0], food[1], self.letter_food)

        while key != 27:  # While they Esc key is not pressed
            window.border('|', '|', '-', '-', '+', '+', '+', '+')

            # Display the score and title
            window.addstr(0, 2, f'Score: {str(self.score)} ')
            window.addstr(0, round(self.width / 2), ' SNAKE! ')

            # Make the snake faster as it eats more
            window.timeout(round(140 - (len(snake) / 5 + len(snake) / 10) % 120))

            event = window.getch()  # Refreshes the screen and then waits for the user to hit a key
            key = key if event == -1 else event

            # Calculates the new coordinates of the head of the snake.
            snake.insert(0, [snake[0][0] + (key == curses.KEY_DOWN and 1) + (key == curses.KEY_UP and -1), snake[0][1] + (key == curses.KEY_LEFT and -1) + (key == curses.KEY_RIGHT and 1)])

            # Exit if snake crosses the boundaries
            if snake[0][0] == 0 or snake[0][0] == self.height - 1 or snake[0][1] == 0 or snake[0][1] == self.width - 1: break

            #Exit if snake runs over itself
            if snake[0] in snake[1:]: break

            # When snake eats the food
            if snake[0] == food:
                food = []
                self.score += 1
                while not food:
                    # Generate coordinates for next food
                    food = [randint(1, self.height - 2), randint(1, self.width - 2)]

                    if food in snake: food = []

                self.display_food(window, food[0], food[1], self.letter_food)
            else:
                last = snake.pop()
                self.display_food(window, last[0], last[1], ' ')
            self.display_food(window, snake[0][0], snake[0][1], self.letter_player)

        curses.endwin()
        self.end_game()


run = True
while run:
    txt = input("Une partie ? (o|n) (c pour custom) : ")

    if txt.lower() == "o":
        SnaKe(h=30, w=60).NewGame()
    elif txt.lower() == "n":
        run = False
    elif txt.lower() == "c":
        size = int(input("Taille du terrain (10 Minimum) : "))
        SnaKe(h=size, w=size*2).NewGame()
    else:
        print("Saisie incorect !")
