#! /usr/bin/env python3
# coding: utf-8

import os
import time
import pickle
import termios
import tty
import sys

from Fonctions.Variables import *
from Fonctions.Variables_Map_Building import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *
from Fonctions.GenerateMaze import *


class GameScreen:

    def __init__(self, maze, start_menu):
        self.maze = maze
        self.start_menu = start_menu
        self.extract(self.maze)
        self.txt_color = WHITE_TEXT

    def start(self):
        """Initiate the variables at the start of the maze"""
        self.maze_on = True
        self.player_have_key = False
        self.time_start = 0
        self.time_spent = ""
        self.margin = 0
        self.margin_v = 0
        self.time_total = 0
        self.timer_start()
        self.time_limit = ((self.height * self.width)//20) + 25
        self.hint = 0
        self.turn_count = 0

    def extract(self, maze):
        """Extract game data from the map"""
        lines = maze.split("\n")
        join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
        props = []
        players = []
        check_player = False
        check_end = False
        check_key = False
        for i, line in enumerate(lines):
            for j, letter in enumerate(line):
                if letter is LETTER_PLAYER[0]:
                    players.append(Player(i, j))
                    props.append(Corridor(i, j))
                    check_player = True
                elif letter is LETTER_PLAYER[1]:
                    players.append(Player(i, j, player_number=2))
                    props.append(Corridor(i, j))
                elif letter is LETTER_END:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j+1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j-1] not in join_with:
                            vertical = True
                    props.append(Door(i, j, vertical, end=True))
                    self.position_end = (i, j)
                    check_end = True
                elif letter is LETTER_DOOR:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j + 1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j - 1] not in join_with:
                            vertical = True
                    props.append(Door(i, j, vertical))
                elif letter is LETTER_WALL:
                    neighbors = ""
                    if i > 0:
                        if lines[i - 1][j] in join_with:
                            neighbors += "N"
                    if i < (len(lines) - 2):
                        if lines[i + 1][j] in join_with:
                            neighbors += "S"
                    if j < (len(lines[0]) - 1):
                        if lines[i][j + 1] in join_with:
                            neighbors += "E"
                    if j > 0:
                        if lines[i][j - 1] in join_with:
                            neighbors += "W"
                    props.append(Wall(i, j, neighbors))
                elif letter is LETTER_KEY:
                    props.append(Corridor(i, j, has_key=True))
                    self.position_key = (i, j)
                    check_key = True
                else:
                    props.append(Corridor(i, j))
        if check_player and check_end and check_key:
            self.players = players
            self.props = props
            self.height = i
            self.width = j
        else:
            self.extract(DEFAULT_MAP)

    def save_game(self):
        """Save the game"""
        with open(SAVE_FILE, "wb") as save_file:
            save_file.write(pickle.dumps(self))

    def display(self):
        """Update and display the maze"""
        if self.start_menu.difficulty == 2 and self.maze_on:
            for item in self.props:
                item.revealed = False
        elif self.start_menu.difficulty == 0:
            for item in self.props:
                item.revealed = True
        offset = 3
        if self.width < len(MESSAGE_MOVES):
            offset = 4
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        if (
                (int(self.rows) < self.height + offset) or
                (int(self.columns) < self.width + 1)):
            print(
                    "\033[8;{0};{1}t"
                    .format(self.height + offset, self.width+1) +
                    CLR_ATTR)
        w = self.width + 1
        # turn off the light near players
        for player in self.players:
            for i in range(-3, 4):
                for j in range(-3, 4):
                    position = (player.y + i) * w + (player.x + j)
                    if 0 <= position < len(self.props):
                        self.props[position].lit = False
        # light surrounding of players
        for player in self.players:
            range_left = -1
            range_right = 2
            if player.x < 1:
                range_left = player.x * -1
            if player.x > (w - 2):
                range_right = w - player.x
            for i in range(-2, 3):
                for j in range(range_left, range_right):
                    position = (player.y + i) * w + (player.x + j)
                    if 0 <= position < len(self.props):
                        self.props[position].lit = True
            range_left = -2
            range_right = 3
            if player.x < 2:
                range_left = player.x * -1
            if player.x > (w - 3):
                range_right = w - player.x
            for i in range(-1, 2):
                for j in range(range_left, range_right):
                    position = (player.y + i) * w + (player.x + j)
                    if 0 <= position < len(self.props):
                        self.props[position].lit = True
            # mark position
            position = (player.y) * w + (player.x)
            self.props[position].visited = True
        # give hint after time limit
        if not self.start_menu.difficulty == 2:
            if self.time_total > self.time_limit and self.hint < 1:
                self.hint = 1
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        position = (
                                (self.position_key[0] + i) * w +
                                (self.position_key[1] + j))
                        if 0 <= position < len(self.props):
                            self.props[position].revealed = True
            if self.time_total > (self.time_limit * 2) and self.hint < 2:
                self.hint = 2
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        position = (
                                (self.position_end[0] + i) * w +
                                (self.position_end[1] + j))
                        if 0 <= position < len(self.props):
                            self.props[position].revealed = True
        # Calculate line of sight
        max_sight = 15
        matrice = (
                ((0,  0, -1, 0),  (0, -1, -1,  0),  (0, 1, -1, 0)),
                ((0,  0,  1, 0),  (0, -1,  1,  0),  (0, 1,  1, 0)),
                ((-1, 0,  0, 0), (-1,  0,  0, -1), (-1, 0,  0, 1)),
                ((1,  0,  0, 0),  (1,  0,  0, -1),  (1, 0,  0, 1)))
        if self.maze_on:  # do not remove or bug
            for player in self.players:
                x = player.x
                y = player.y
                self.props[(y * w) + (x)].revealed = True
                for n in matrice:
                    i = 1
                    j = 1
                    side1 = side2 = lenght = max_sight
                    while i < lenght:
                        item = self.props[(
                                ((y + (i * n[0][0]) + (j * n[0][1])) * w) +
                                (x + (i * n[0][2]) + (j * n[0][3])))]
                        if not item.sight:
                            lenght = i
                        item.revealed = True
                        j = 1
                        while j < side1:
                            side_item = self.props[(
                                    ((y + (i * n[1][0]) + (j * n[1][1])) * w) +
                                    (x + (i * n[1][2]) + (j * n[1][3])))]
                            j += 1
                            if not side_item.sight:
                                side1 = j
                            side_item.revealed = True
                        j = 1
                        while j < side2:
                            side_item = self.props[(
                                    ((y + (i * n[2][0]) + (j * n[2][1])) * w) +
                                    (x + (i * n[2][2]) + (j * n[2][3])))]
                            j += 1
                            if not side_item.sight:
                                side2 = j
                            side_item.revealed = True
                        i += 1
        to_reveal = []
        for player in self.players:
            for i in range(max_sight * -1, max_sight + 1):
                for j in range(max_sight * -1, max_sight + 1):
                    position = (player.y + i) * w + (player.x + j)
                    if 0 <= position < len(self.props):
                        item = self.props[position]
                    else:
                        continue
                    if item.y < self.height - 1:
                        test_item = self.props[((item.y + 1) * w) + (item.x)]
                        if (
                                test_item.revealed and not
                                item.sight and test_item.sight):
                            to_reveal.append(item)
                    if item.y > 0:
                        test_item = self.props[((item.y - 1) * w) + (item.x)]
                        if (
                                test_item.revealed and not
                                item.sight and test_item.sight):
                            to_reveal.append(item)
                    if item.x < self.width:
                        test_item = self.props[((item.y) * w) + (item.x + 1)]
                        if (
                                test_item.revealed and not
                                item.sight and test_item.sight):
                            to_reveal.append(item)
                    if item.x > 0:
                        test_item = self.props[((item.y) * w) + (item.x - 1)]
                        if (
                                test_item.revealed and not
                                item.sight and test_item.sight):
                            to_reveal.append(item)
        for item in to_reveal:
            item.revealed = True
        for player in self.players:
            for i in range(max_sight * -1, max_sight + 1):
                for j in range(max_sight * -1, max_sight + 1):
                    position = (player.y + i) * w + (player.x + j)
                    if 0 <= position < len(self.props):
                        item = self.props[position]
                    else:
                        continue
                    revealed_wall_count = []
                    if item.y < self.height - 1:
                        test_item = self.props[((item.y + 1) * w) + (item.x)]
                        if (
                                test_item.revealed and not
                                test_item.sight and not item.sight):
                            revealed_wall_count.append(item)
                    if item.y > 0:
                        test_item = self.props[((item.y - 1) * w) + (item.x)]
                        if (
                                test_item.revealed and not
                                test_item.sight and not item.sight):
                            revealed_wall_count.append(item)
                    if item.x < self.width:
                        test_item = self.props[((item.y) * w) + (item.x + 1)]
                        if (
                                test_item.revealed and not
                                test_item.sight and not item.sight):
                            revealed_wall_count.append(item)
                    if item.x > 0:
                        test_item = self.props[((item.y) * w) + (item.x - 1)]
                        if (
                                test_item.revealed and not
                                test_item.sight and not item.sight):
                            revealed_wall_count.append(item)
                    if len(revealed_wall_count) == 2:
                        item.revealed = True

        self.margin = ((int(self.columns) - self.width)//2)
        self.margin_v = ((int(self.rows) - self.height)//2)

        # if self.turn_count % 5 == 0:  NO. Blinky.
        if True:
            maze_map = (
                    CLEAR_SCREEN +
                    "\033[{};0H".format(self.margin_v) +
                    " " * self.margin +
                    CLR_ATTR)
            for item in self.props:
                maze_map += str(item)
                if item.x == self.width:
                    maze_map += "\n" + " " * self.margin
            print(maze_map)
        else:
            for player in self.players:
                for i in range((max_sight + 2) * -1, (max_sight + 2) + 1):
                    for j in range(max_sight * -1, max_sight + 1):
                        position = (player.y + i) * w + (player.x + j)
                        if 0 <= position < len(self.props):
                            item = self.props[position]
                        else:
                            continue
                        self.props[position]\
                            .display(self.margin, self.margin_v)
        self.turn_count += 1
        for player in self.players:
            player.display(self.margin, self.margin_v)
        if self.player_have_key:
            margin = ((int(self.columns) - len(SYMBOL_KEY) + 4)//2)
            if margin < 0:
                margin = 0
            print(
                    B_WHITE_TEXT +
                    "\033[{0};{1}H{2}\033[1B"
                    .format(self.height + self.margin_v, margin, SYMBOL_KEY) +
                    CLR_ATTR)
        else:
            margin = ((int(self.columns) - len(MESSAGE_KEY) + 4)//2)
            if margin < 0:
                margin = 0
            print(
                    self.txt_color +
                    "\033[{0};{1}H{2}\033[1B"
                    .format(self.height + self.margin_v, margin, MESSAGE_KEY) +
                    CLR_ATTR)
        if len(self.players) > 1:
            margin = ((int(self.columns) - (len(MESSAGE_MOVES_MULTI)-30))//2)
            message_moves = MESSAGE_MOVES_MULTI
        else:
            margin = ((int(self.columns) - len(MESSAGE_MOVES) + 4)//2)
            message_moves = MESSAGE_MOVES
        if margin < 0:
            margin = 0
        print(
                self.txt_color +
                "\033[{0};{1}H{2}"
                .format(
                    self.height + 1 + self.margin_v,
                    margin,
                    message_moves) +
                CLR_ATTR)
        self.timer_add()
        self.save_game()
        self.timer_start()

    def player_move(self):
        """Detect keystrokes and move the player accordingly"""
        no_input = True
        player_to_move = 0
        movement = ""
        cheatcode = 0
        while no_input:
            keystroke = self.keyboard_input(1)
            if keystroke == CTRL_C:
                os.system('clear')
                exit()
            elif ord(keystroke) == BACKSPACE:
                no_input = False
                self.maze_on = False
                self.start_menu.chosen = False
            elif keystroke.lower() == 'p':
                cheatcode = 1
            elif keystroke.lower() == 'o' and cheatcode == 1:
                cheatcode = 2
            elif keystroke.lower() == 'u' and cheatcode == 2:
                cheatcode = 3
            elif keystroke.lower() == 'e' and cheatcode == 3:
                cheatcode = 4
            elif keystroke.lower() == 't' and cheatcode == 4:
                self.start_menu.difficulty = 0
                self.turn_count = 0
                no_input = False
            # elif keystroke.lower()=='g':
            #     for item in self.props:
            #         item.symbol = SYMBOL_WALL
            #     no_input = False
            elif keystroke.lower() == KEY_UP_PLAYER_2:
                player_to_move = 2
                movement = "U"
                no_input = False
            elif keystroke.lower() == KEY_DOWN_PLAYER_2:
                player_to_move = 2
                movement = "D"
                no_input = False
            elif keystroke.lower() == KEY_RIGHT_PLAYER_2:
                player_to_move = 2
                movement = "R"
                no_input = False
            elif keystroke.lower() == KEY_LEFT_PLAYER_2:
                player_to_move = 2
                movement = "L"
                no_input = False
            elif keystroke == ESCAPE_CHARACTER:
                addendum = self.keyboard_input(2)
                keystroke = keystroke + addendum
            if keystroke == ARROW_UP:
                player_to_move = 1
                movement = "U"
                no_input = False
            elif keystroke == ARROW_DOWN:
                player_to_move = 1
                movement = "D"
                no_input = False
            elif keystroke == ARROW_RIGHT:
                player_to_move = 1
                movement = "R"
                no_input = False
            elif keystroke == ARROW_LEFT:
                player_to_move = 1
                movement = "L"
                no_input = False

        for player in self.players:
            player.move(player_to_move, movement, self.props, self.width)

    def tests(self):
        """Unlock end door if the key was picked and end the game if the player
        has reached the exit"""
        w = self.width + 1
        for player in self.players:
            position_player = (player.y, player.x)
            if position_player == self.position_key:
                self.player_have_key = True
                position = (self.position_end[0] * w + self.position_end[1])
                self.props[position].block = False
                position = (self.position_key[0] * w + self.position_key[1])
                self.props[position].has_key = False
            if position_player == self.position_end:
                self.maze_on = False
                self.finished_menu()

    def timer_start(self):
        """Start the timer"""
        self.time_start = time.time()

    def timer_add(self):
        """add time played since the last turn to total"""
        self.time_total += time.time() - self.time_start

    def timer_stop(self):
        """Stop the timer"""
        self.timer_add()
        minutes = int(self.time_total // 60)
        seconds = int(self.time_total % 60)
        hours = minutes // 60
        minutes == minutes % 60
        if seconds <= 1:
            word_seconds = WORD_SECOND
        else:
            word_seconds = WORD_SECONDS
        if minutes <= 1:
            word_minutes = WORD_MINUTE
        else:
            word_minutes = WORD_MINUTES
        if not minutes and not hours:
            self.time_spent = "{0} {1}".format(seconds, word_seconds)
        elif not hours:
            self.time_spent = (
                "{0} {1}, {2} {3}"
                .format(minutes, word_minutes, seconds, word_seconds))
        else:
            self.time_spent = MESSAGE_HOUR_LONG

    def save_maze(self):
        """Save the maze (map)"""
        go_for_save = False
        while not go_for_save:
            margin = ((int(self.columns) - len(MESSAGE_SAVE_MAZE))//2)
            if margin < 0:
                margin = 0
            maze_file = input(
                self.txt_color +
                "\033[{0};0H\033[K\033[{1}C{2}\n\033[K\033[{1}C".format(
                    self.height + self.margin_v,
                    margin,
                    MESSAGE_SAVE_MAZE))
            maze_file = MAPS_DIRECTORY + maze_file + MAPS_FORMAT
            if os.path.exists(maze_file):
                print(
                    "\033[{0};0H\033[K\033[{1}C{2}\n\033[K\033[{1}C{3}".format(
                        self.height + self.margin_v,
                        margin,
                        MESSAGE_SAVE_OVERWRITE_1,
                        MESSAGE_SAVE_OVERWRITE_2))
                keystroke = self.keyboard_input(1)
                if keystroke == 'CTRL_C':
                    os.system('clear')
                    exit()
                elif keystroke.lower() == 'o' or keystroke.lower() == 'y':
                    go_for_save = True
                elif ord(keystroke) == BACKSPACE:
                    break
            else:
                go_for_save = True
        if go_for_save:
            with open(maze_file, "w") as save_file:
                save_file.write(self.maze)

    def print_path_taken(self):
        """Print the path players had taken"""
        for item in self.props:
            if (type(item) == Corridor) and item.visited:
                print(
                    "{0}\033[{1};{2}H{3}".format(
                        B_BLUE_TEXT,
                        item.y + self.margin_v,
                        item.x + 1 + self.margin,
                        SYMBOL_CORRIDOR_VISITED))
        for player in self.players:
            player.display(self.margin, self.margin_v)

    def keyboard_input(self, nbl):
        """Capture keystrokes"""
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab = sys.stdin.read(nbl)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return text_grab

    def finished_menu(self):
        """Display the end menu"""
        for item in self.props:
            item.revealed = True
        self.turn_count = 0
        self.display()
        os.remove(SAVE_FILE)
        self.timer_stop()
        self.print_path_taken()
        steps = 0
        for player in self.players:
            steps += player.step
        map_already_saved = False
        if self.start_menu.selected == 0:
            map_already_saved = True
        margin = ((int(self.columns) - len(MESSAGE_WIN_1))//2)
        if margin < 0:
            margin = 0
        print(
            self.txt_color +
            "\033[{0};{1}H{2}".format(
                self.height + self.margin_v,
                margin,
                MESSAGE_WIN_1.format(self.time_spent, steps)))
        if map_already_saved:
            message = MESSAGE_WIN_2_SAVED
        else:
            message = MESSAGE_WIN_2
        margin = ((int(self.columns) - len(message)+8)//2)
        if margin < 0:
            margin = 0
        print(
            self.txt_color +
            "\033[{0};0H\033[K\033[{1}C{2}"
            .format(self.height + 1 + self.margin_v, margin, message))
        no_input = True
        while no_input:
            keystroke = self.keyboard_input(1)
            if keystroke == CTRL_C:
                os.system('clear')
                exit()
            elif ord(keystroke) == BACKSPACE:
                no_input = False
                self.start_menu.chosen = False
            elif ord(keystroke) == ENTER and not map_already_saved:
                no_input = False
            elif keystroke.lower() == "k":
                if map_already_saved:
                    margin = (
                        (int(self.columns) -
                            len(MESSAGE_MAP_ALREADY_SAVED)) // 2)
                    if margin < 0:
                        margin = 0
                    print(
                        "\033[{0};0H\033[K\033[{1}C{2}".format(
                            self.height + self.margin_v,
                            margin,
                            MESSAGE_MAP_ALREADY_SAVED))
                else:
                    self.save_maze()
                    no_input = False
                self.start_menu.chosen = False
