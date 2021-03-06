#! /usr/bin/env python3
# coding: utf-8

import glob
import termios
import tty
import sys
import os

from Fonctions.Variables import *
from Fonctions.GenerateMaze import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *
from Fonctions.Title import *


class StartMenu():
    def __init__(self):
        self.selected = 0
        self.chosen = False
        self.file_index = 0
        self.choice = []
        self.file_path = MAPS_LOAD.find("*")
        self.difficulty = 1
        self.number_of_players = 1
        self.x = 20
        self.y = 10
        self.directory_content = glob.glob(MAPS_LOAD)
        if not self.directory_content:
            self.selected = 1
            self.min_choice = 1
        else:
            self.min_choice = 0

    def __str__(self):
        if not self.directory_content:
            self.saved_maps = (
                MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY) +
                CLR_ATTR)
        else:
            self.saved_maps = (
                MESSAGE_MAP_LOAD +
                self.directory_content[self.file_index][self.file_path:-4]
                .capitalize())
        self.choice = [self.saved_maps] + [
            MESSAGE_MAP_CHOICE_RANDOM_SMALL,
            MESSAGE_MAP_CHOICE_RANDOM_BIG,
            MESSAGE_MAP_CHOICE_RANDOM_SCREEN,
            MESSAGE_SET_SIZE.format(self.x + 1, self.y + 1),
            MESSAGE_DIFFICULTY_COLORS[self.difficulty] +
            MESSAGE_DIFFICULTY[self.difficulty],
            B_WHITE_TEXT + MESSAGE_NUMBER_PLAYERS[self.number_of_players - 1],
            MESSAGE_MAP_CHOICE_QUIT]
        result_str = ""
        for i, maze_map in enumerate(self.choice):
            if i == self.selected and 5 <= self.selected <= 6:
                result_str += "\033[4m" + maze_map + CLR_ATTR
            elif i == self.selected:
                result_str += BLACK_ON_WHITE + maze_map + CLR_ATTR
            else:
                if maze_map == MESSAGE_MAP_CHOICE_QUIT:
                    result_str += B_RED_TEXT + maze_map + CLR_ATTR
                else:
                    result_str += WHITE_TEXT + maze_map + CLR_ATTR
            result_str += "\n"
        return result_str

    def maze_menu(self):
        """Maze selection menu"""
        self.extract(make_maze(30, 15))
        # keystroke = 0
        while not self.chosen:
            title_screen_maze = ""
            for item in self.props:
                item.revealed = True
                title_screen_maze += str(item)
                if item.x == self.width:
                    title_screen_maze += "\n"
            print(CLEAR_SCREEN + CURSOR_RESET + title_screen_maze)
            print("\033[5;6H " + B_GREEN_TEXT + TITLE_1)
            print("\033[6;6H " + B_GREEN_TEXT + TITLE_2)
            print("\033[7;6H " + B_GREEN_TEXT + TITLE_3)
            print("\033[8;6H " + B_GREEN_TEXT + TITLE_4)
            print("\033[9;6H " + B_GREEN_TEXT + TITLE_5)
            print("\033[10;6H " + B_GREEN_TEXT + TITLE_6)
            print("\033[11;17H " + B_BLUE_TEXT + TITLE_7)
            print("\033[12;17H " + B_BLUE_TEXT + TITLE_8)
            print("\033[13;17H " + B_BLUE_TEXT + TITLE_9)
            print("\033[17;0H" + B_BLUE_TEXT + MESSAGE_MAP_CHOICE + CLR_ATTR)
            print(self)
            # print(keystroke,self.selected,len(self.choice))
            no_input = True
            while no_input:
                keystroke = self.keyboard_input(1)
                if keystroke == CTRL_C or ord(keystroke) == BACKSPACE:
                    os.system('clear')
                    exit()
                elif ord(keystroke) == ENTER and self.selected in (5, 6):
                    self.extract(make_maze(30, 15))
                    no_input = False
                elif ord(keystroke) == ENTER:
                    self.chosen = self.choice[self.selected]
                    no_input = False
                elif keystroke == ESCAPE_CHARACTER:
                    addendum = self.keyboard_input(2)
                    keystroke = keystroke + addendum
                elif ord(keystroke) == SPACE and self.selected == 4:
                    self.set_size()
                    no_input = False
                elif ord(keystroke) == SPACE:
                    self.extract(make_maze(30, 15))
                    no_input = False
                if keystroke == ARROW_DOWN:
                    no_input = False
                    if self.selected < (len(self.choice)-1):
                        self.selected += 1
                    else:
                        self.selected = self.min_choice
                elif keystroke == ARROW_UP:
                    no_input = False
                    if self.selected > self.min_choice:
                        self.selected -= 1
                    else:
                        self.selected = len(self.choice)-1
                elif keystroke == ARROW_LEFT:
                    no_input = False
                    if self.selected == 0 and self.file_index > 0:
                        self.file_index -= 1
                    elif self.selected == 5 and self.difficulty > 0:
                        self.difficulty -= 1
                    elif self.selected == 5 and self.difficulty == 0:
                        self.difficulty = len(MESSAGE_DIFFICULTY)-1
                    elif self.selected == 6 and self.number_of_players == 1:
                        self.number_of_players = 2
                    elif self.selected == 6 and self.number_of_players == 2:
                        self.number_of_players = 1
                elif keystroke == ARROW_RIGHT:
                    no_input = False
                    if (
                            self.selected == 0 and
                            self.file_index < len(self.directory_content) - 1):
                        self.file_index += 1
                    elif (
                            self.selected == 5 and
                            self.difficulty < len(MESSAGE_DIFFICULTY) - 1):
                        self.difficulty += 1
                    elif (
                            self.selected == 5 and
                            self.difficulty == len(MESSAGE_DIFFICULTY) - 1):
                        self.difficulty = 0
                    elif self.selected == 6 and self.number_of_players == 1:
                        self.number_of_players = 2
                    elif self.selected == 6 and self.number_of_players == 2:
                        self.number_of_players = 1
        if self.chosen == self.saved_maps and self.directory_content:
            self.chosen = self.directory_content[self.file_index]
            if os.path.exists(self.chosen):
                with open(self.chosen, "r") as maze_map:
                    return maze_map.read()
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SMALL:
            maze_map = make_maze(
                SMALL_WIDTH,
                SMALL_HEIGHT,
                number_of_players=self.number_of_players)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG:
            maze_map = make_maze(
                BIG_WIDTH,
                BIG_HEIGHT,
                number_of_players=self.number_of_players)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SCREEN:
            rows, columns = os.popen('stty size', 'r').read().split()
            maze_map = make_maze(
                int(columns)-1,
                int(rows)-4,
                number_of_players=self.number_of_players)
            return maze_map
        elif self.chosen == MESSAGE_SET_SIZE.format(self.x + 1, self.y + 1):
            maze_map = make_maze(
                self.x,
                self.y,
                number_of_players=self.number_of_players)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_QUIT:
            os.system('clear')
            exit()
        else:
            self.chosen = False

    def keyboard_input(self, nbl):
        """Capture keystrokes"""
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab = sys.stdin.read(nbl)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return text_grab

    def extract(self, maze):
        """Extract data from map"""
        lines = maze.split("\n")
        join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
        props = []
        for i, line in enumerate(lines):
            for j, letter in enumerate(line):
                if letter is LETTER_PLAYER[0]:
                    props.append(Corridor(i, j))
                elif letter is LETTER_END:
                    vertical = False
                    if j < len(line) - 1:
                        if lines[i][j + 1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j - 1] not in join_with:
                            vertical = True
                    props.append(Door(i, j, vertical, end=True))
                elif letter is LETTER_DOOR:
                    vertical = False
                    if j < len(line) - 1:
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
                else:
                    props.append(Corridor(i, j))
        self.props = props
        self.height = i
        self.width = j
        self.maze = maze

    def set_size(self):
        choosing = True
        while choosing:
            self.rows, self.columns = os.popen('stty size', 'r').read().split()
            self.extract(make_maze(self.x, self.y))
            self.margin = ((int(self.columns) - self.width) // 2)
            self.margin_v = ((int(self.rows) - self.height) // 2)
            maze_map = (
                CLEAR_SCREEN +
                "\033[{};0H".format(self.margin_v) +
                " " * self.margin +
                CLR_ATTR)
            for item in self.props:
                item.revealed = True
                maze_map += str(item)
                if item.x == self.width:
                    maze_map += "\n" + " " * self.margin
            print(maze_map)
            margin = ((int(self.columns) - len(MESSAGE_CONTROLS_SIZE) + 4)//2)
            if margin < 0:
                margin = 0
            print(
                WHITE_TEXT +
                "\033[{0};{1}H{2}\033[1B".format(
                    self.height + self.margin_v,
                    margin,
                    MESSAGE_CONTROLS_SIZE) +
                CLR_ATTR)
            no_input = True
            while no_input:
                keystroke = self.keyboard_input(1)
                if keystroke == CTRL_C:
                    os.system('clear')
                    exit()
                elif ord(keystroke) == ENTER or ord(keystroke) == BACKSPACE:
                    choosing = False
                    no_input = False
                    self.extract(make_maze(30, 15))
                elif keystroke == ESCAPE_CHARACTER:
                    addendum = self.keyboard_input(2)
                    keystroke = keystroke + addendum
                if keystroke == ARROW_DOWN and self.y > 6:
                    self.y -= 2
                    no_input = False
                elif keystroke == ARROW_UP and self.y < int(self.rows) - 8:
                    self.y += 2
                    no_input = False
                elif keystroke == ARROW_LEFT and self.x > 6:
                    self.x -= 2
                    no_input = False
                elif (
                        keystroke == ARROW_RIGHT and
                        self.x < int(self.columns) - 8):
                    self.x += 2
                    no_input = False
