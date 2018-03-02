#! /usr/bin/env python3
# coding: utf-8

import glob, termios, tty, sys, os
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

    def __str__(self):
        self.directory_content = glob.glob(MAPS_LOAD)
        self.min_choice = 0
        if not self.directory_content:
            self.saved_maps = (MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY)\
            + CLR_ATTR)
            self.selected = 1
            self.min_choice = 1
        else:
            self.saved_maps = MESSAGE_MAP_LOAD+self.directory_content\
            [self.file_index][self.file_path:-4].capitalize()
        self.choice = [self.saved_maps] + [MESSAGE_MAP_CHOICE_RANDOM_SMALL,\
        MESSAGE_MAP_CHOICE_RANDOM_BIG,\
        MESSAGE_MAP_CHOICE_RANDOM_SCREEN,\
        MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER,\
        MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER,\
        MESSAGE_DIFFICULTY_COLORS[self.difficulty] + \
        MESSAGE_DIFFICULTY[self.difficulty],\
        MESSAGE_MAP_CHOICE_QUIT]
        result_str = ""
        for i, maze_map in enumerate(self.choice):
            if i == self.selected and self.selected == 6:
                result_str += \
                "\033[4m" + maze_map + CLR_ATTR
            elif i == self.selected:
                result_str += \
                BLACK_ON_WHITE + maze_map + CLR_ATTR
            else:
                if maze_map == MESSAGE_MAP_CHOICE_QUIT:
                    result_str += B_RED_TEXT + maze_map + CLR_ATTR
                else:
                    result_str += WHITE_TEXT + maze_map + CLR_ATTR
            result_str += "\n"
        return result_str

    def maze_menu(self):
        """Maze selection menu"""
        self.extract(make_maze(30,15))
        while not self.chosen:
            title_screen_maze = ""
            for item in self.props:
                item.revealed=True
                title_screen_maze += str(item)
                if item.x == self.width:
                    title_screen_maze += "\n"
            print(CLEAR_SCREEN + CURSOR_RESET + title_screen_maze)
            print("\033[5;6H "+ B_GREEN_TEXT + TITLE_1)
            print("\033[6;6H "+ B_GREEN_TEXT + TITLE_2)
            print("\033[7;6H "+ B_GREEN_TEXT + TITLE_3)
            print("\033[8;6H "+ B_GREEN_TEXT + TITLE_4)
            print("\033[9;6H "+ B_GREEN_TEXT + TITLE_5)
            print("\033[10;6H "+ B_GREEN_TEXT + TITLE_6)
            print("\033[11;17H "+ B_BLUE_TEXT + TITLE_7)
            print("\033[12;17H "+ B_BLUE_TEXT + TITLE_8)
            print("\033[13;17H "+ B_BLUE_TEXT + TITLE_9)
            print("\033[17;0H" + B_BLUE_TEXT + MESSAGE_MAP_CHOICE + CLR_ATTR)
            print(self)
            no_input = True
            while no_input:
                choice = self.keyboard_input(1)
                if choice == CTRL_C:
                    os.system('clear')
                    exit()
                elif ord(choice) == ENTER and self.selected != 6:
                    self.chosen = \
                    self.choice[self.selected]
                    no_input = False
                elif choice == ESCAPE_CHARACTER:
                    addendum = self.keyboard_input(2)
                    choice = choice + addendum
                elif ord(choice) == BACKSPACE:
                    os.system('clear')
                    exit()
                elif ord(choice) == SPACE:
                    self.extract(make_maze(30,15))
                    no_input = False
                if choice==ARROW_DOWN:
                    if self.selected < (len(self.choice)-1):
                        self.selected += 1
                    no_input = False
                elif choice==ARROW_UP:
                    if self.selected > self.min_choice:
                        self.selected -= 1
                    no_input = False
                elif choice==ARROW_LEFT:
                    no_input = False
                    if self.selected == 0 and self.file_index > 0:
                        self.file_index -= 1
                    if self.selected == 6 and self.difficulty > 0:
                        self.difficulty -= 1
                    else:
                        self.difficulty = len(MESSAGE_DIFFICULTY)-1
                elif choice==ARROW_RIGHT:
                    no_input = False
                    if self.selected == 0 \
                    and self.file_index<len(self.directory_content)-1:
                        self.file_index += 1
                    if self.selected == 6 \
                    and self.difficulty < len(MESSAGE_DIFFICULTY)-1:
                        self.difficulty += 1
                    else:
                        self.difficulty = 0
        if self.chosen == self.saved_maps and self.directory_content:
            self.chosen = self.directory_content[self.file_index]
            if os.path.exists(self.chosen):
                with open(self.chosen, "r") as maze_map:
                    return maze_map.read()
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SMALL:
            maze_map = make_maze(SMALL_WIDTH,SMALL_HEIGHT)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG:
            maze_map = make_maze(BIG_WIDTH,BIG_HEIGHT)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SCREEN:
            rows, columns = os.popen('stty size', 'r').read().split()
            maze_map = make_maze(int(columns)-1,int(rows)-4)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER:
            maze_map = make_maze(BIG_WIDTH,BIG_HEIGHT, number_of_players=2)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER:
            rows, columns = os.popen('stty size', 'r').read().split()
            maze_map = make_maze(int(columns)-1,int(rows)-4,number_of_players=2)
            return maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_QUIT:
            os.system('clear')
            exit()

    def keyboard_input(self, nbl):
        """Capture keystrokes"""
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab=sys.stdin.read(nbl)
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
                    props.append(Corridor(i,j))
                elif letter is LETTER_END:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j+1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j-1] not in join_with:
                            vertical = True
                    props.append(Door(i,j,vertical,end = True))
                elif letter is LETTER_DOOR:
                    vertical = False
                    if j < len(line)-1:
                        if lines[i][j+1] not in join_with:
                            vertical = True
                    if j > 0:
                        if lines[i][j-1] not in join_with:
                            vertical = True
                    props.append(Door(i,j,vertical))
                elif letter is LETTER_WALL:
                    neighbors = ""
                    if i>0:
                        if lines[i-1][j] in join_with:
                            neighbors += "N"
                    if i<(len(lines)-2):
                        if lines[i+1][j] in join_with:
                            neighbors += "S"
                    if j<(len(lines[0])-1):
                        if lines[i][j+1] in join_with:
                            neighbors += "E"
                    if j>0:
                        if lines[i][j-1] in join_with:
                            neighbors += "W"
                    props.append(Wall(i,j,neighbors))
                elif letter is LETTER_KEY:
                    props.append(Corridor(i,j,has_key=True))
                else:
                    props.append(Corridor(i,j))
        self.props = props
        self.height = i
        self.width = j
        self.maze = maze
