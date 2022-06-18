import curses
import datetime
import os
import shutil
from random import randint
import utils

GUID = str(os.getenv("USERNAME"))
JSON_USERS = "F:\\ADOBE\\Creative Cloud Files\\01_PROJETS\\01_PROG\\01_PYTHON\\Formation\\01_Python\\TP\\06_Snake\\users.json"
LEADERBOARD_TEMP = "F:\\ADOBE\\Creative Cloud Files\\01_PROJETS\\01_PROG\\01_PYTHON\\Formation\\01_Python\\TP\\06_Snake\\leaderboard\\__TEMP__.json"
LEADERBOARD = "F:\\ADOBE\\Creative Cloud Files\\01_PROJETS\\01_PROG\\01_PYTHON\\Formation\\01_Python\\TP\\06_Snake\\leaderboard\\"


class SnaKe:
    def __init__(self, h, w):
        self.letter_player = "#"
        self.letter_food = "O"
        self.wall = "#"
        self.corner = "@"
        self.height = h
        self.width = w
        self.user = ""
        self.score = 0

        self.leaderboard_file = f"{LEADERBOARD}leaderboard_{self.height}_{self.width}.json"

        self.init_player()
        self.init_leaderboard()

    def init_player(self):
        data = utils.open_json(JSON_USERS)
        self.user = data.get(GUID)

        if self.user is None:
            utils.update_json(JSON_USERS, {GUID: GUID})
            self.user = GUID

    def init_leaderboard(self):
        False if os.path.exists(self.leaderboard_file) else shutil.copyfile(LEADERBOARD_TEMP, self.leaderboard_file)

    def write_log(self, file, score_fin):
        with open(file, "w") as js:
            js.write(f"""Terrain: {self.height}_{self.width}
User: {self.user}
Score: {self.score}""")

    def update_leaderboard(self):
        data = utils.open_json(self.leaderboard_file)

        try:
            best_score = data.get(self.user)
            if self.score <= best_score: return
        except:
            pass

        utils.update_json(self.leaderboard_file, {self.user: self.score})

    def end_game(self):
        score_fin = "\nScore: " + str(self.score)

        self.write_log(
            fr"F:\ADOBE\Creative Cloud Files\01_PROJETS\01_PROG\01_PYTHON\Formation\01_Python\TP\06_Snake\logs\Logs_{self.user}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log",
            score_fin)

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
        window.border(self.wall, self.wall, self.wall, self.wall, self.corner, self.corner, self.corner, self.corner)
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
            # Display the score and title
            window.addstr(0, 2, f'Score: {str(self.score)} ')
            window.addstr(0, round(self.width / 2), ' SNAKE! ')

            # Make the snake faster as it eats more
            window.timeout(round(140 - (len(snake) / 5 + len(snake) / 10) % 120))

            event = window.getch()  # Refreshes the screen and then waits for the user to hit a key
            key = key if event == -1 else event

            # Calculates the new coordinates of the head of the snake.
            snake.insert(0, [snake[0][0] + (key == curses.KEY_DOWN and 1) + (key == curses.KEY_UP and -1),
                             snake[0][1] + (key == curses.KEY_LEFT and -1) + (key == curses.KEY_RIGHT and 1)])

            # Exit if snake crosses the boundaries
            if snake[0][0] == 0 or snake[0][0] == self.height - 1 or snake[0][1] == 0 or snake[0][
                1] == self.width - 1: break

            # Exit if snake runs over itself
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
        SnaKe(h=size, w=size * 2).NewGame()
    else:
        print("Saisie incorrect !")
