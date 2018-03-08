#! /usr/bin/env python3
# coding: utf-8

import glob, termios, tty, sys, os

from Fonctions.Variables import *
from Fonctions.GenerateMaze import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *



class Editor():
    def __init__(self):
        self.selected = 0
        self.chosen = False
        self.file_index = 0
        self.choice = []
        self.file_path = MAPS_LOAD.find("*")
        self.maze = ""
        self.x = 0
        self.y = 0
        self.edit_on = True

    def __str__(self):
        self.directory_content = glob.glob(MAPS_LOAD)
        self.min_choice = 0
        if not self.directory_content:
            self.saved_maps = (MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY) \
            + CLR_ATTR)
            self.selected = 1
            self.min_choice = 1
        else:
            self.saved_maps = MESSAGE_MAP_LOAD+self.directory_content\
            [self.file_index][self.file_path:-4].capitalize() + CLR_ATTR
        self.choice = [self.saved_maps] + [MESSAGE_MAP_CHOICE_RANDOM_SMALL, \
        MESSAGE_MAP_CHOICE_RANDOM_BIG, MESSAGE_MAP_CHOICE_DEFINE_SIZE, \
        MESSAGE_MAP_CHOICE_QUIT]
        result_str = ""
        for i, maze_map in enumerate(self.choice):
            if i == self.selected:
                result_str += \
                BLACK_ON_WHITE + maze_map + WHITE_TEXT + CLR_ATTR
            else:
                if maze_map == MESSAGE_MAP_CHOICE_QUIT:
                    result_str += B_RED_TEXT + maze_map + CLR_ATTR
                else:
                    result_str += WHITE_TEXT + maze_map + CLR_ATTR
            result_str += "\n"
        return result_str

    def maze_menu(self):
        while not self.chosen:
            no_input = True
            while no_input:
                print(CLEAR_SCREEN + CURSOR_RESET)
                print(self)
                keystroke = self.keyboard_input(1)
                if keystroke == CTRL_C or ord(keystroke) == BACKSPACE:
                    os.system('clear')
                    exit()
                elif ord(keystroke) == ENTER:
                    self.chosen = \
                    self.choice[self.selected]
                    no_input = False
                elif keystroke == ESCAPE_CHARACTER:
                    addendum = self.keyboard_input(2)
                    keystroke = keystroke + addendum
                if keystroke == ARROW_DOWN:
                    if self.selected < (len(self.choice)-1):
                        self.selected += 1
                    no_input = False
                elif keystroke == ARROW_UP:
                    if self.selected > self.min_choice:
                        self.selected -= 1
                    no_input = False
                elif keystroke == ARROW_LEFT and self.file_index > 0 \
                and self.selected == 0:
                    self.file_index -= 1
                    no_input = False
                elif keystroke == ARROW_RIGHT and self.selected == 0 \
                and self.file_index<len(self.directory_content)-1:
                    self.file_index += 1
                    no_input = False
        if self.chosen == self.saved_maps and self.directory_content:
            self.chosen = self.directory_content[self.file_index]
            if os.path.exists(self.chosen):
                with open(self.chosen, "r") as maze_map:
                    self.maze = maze_map.read()
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_SMALL:
            maze_map = make_maze(SMALL_WIDTH,SMALL_HEIGHT)
            self.maze = maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_RANDOM_BIG:
            maze_map = make_maze(BIG_WIDTH,BIG_HEIGHT)
            self.maze = maze_map
        elif self.chosen == MESSAGE_MAP_CHOICE_DEFINE_SIZE:
            w = input(MESSAGE_WIDTH)
            h = input(MESSAGE_HEIGHT)
            try:
                maze_map = make_maze(int(w),int(h))
                self.maze = maze_map
            except:
                pass
        elif self.chosen == MESSAGE_MAP_CHOICE_QUIT:
            os.system('clear')
            exit()

    def display(self):
        lines = self.maze.split("\n")
        join_with = (LETTER_WALL, LETTER_DOOR, LETTER_END)
        props = []
        players = []
        for i, line in enumerate(lines):
            for j, letter in enumerate(line):
                if letter is LETTER_PLAYER[0]:
                    players.append(Player(i,j))
                    props.append(Corridor(i,j))
                elif letter is LETTER_PLAYER[1]:
                    players.append(Player(i,j,player_number = 2))
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
        self.players = players
        self.props = props
        self.height = i
        self.width = j
        maze_map = ""
        for item in self.props:
            if (item.x,item.y) == (self.x,self.y):
                maze_map += "\033[7m"
            is_not_player = True
            item.revealed = True
            for player in players:
                if (item.x,item.y) == (player.x,player.y):
                    is_not_player = False
                    if player.player_number == 1:
                        color = B_BLUE_TEXT
                    else:
                        color = B_RED_TEXT
                    maze_map += color + SYMBOL_PLAYER + CLR_ATTR
            if is_not_player:
                maze_map += str(item)
            if (item.x,item.y) == (self.x,self.y):
                maze_map += CLR_ATTR
            if item.x == self.width:
                maze_map += "\n"
        print(CLEAR_SCREEN + CURSOR_RESET + maze_map)
        print("\033[{0};0H{1},{2}".format(self.height + 1,self.x,self.y))
        print(MESSAGE_EDITOR_KEYS)

    def delete_maze_walls(self, maze_map):
        print(MESSAGE_DELETE_MAZE_WALLS)
        keystroke = self.keyboard_input(1)
        if keystroke == CTRL_C:
            os.system('clear')
            exit()
        elif keystroke.lower() == 'o' or keystroke.lower() == 'y':
            for i in range(1,self.width):
                for j in range(1,self.height-1):
                    maze_map[j][i]= LETTER_CORRIDOR
        return maze_map


    def edit(self):
        maze_map=[]
        lines = self.maze.split("\n")
        for i, line in enumerate(lines):
            maze_map.append([])
            for letter in line:
                maze_map[i].append(letter)
        no_input = True
        while no_input:
            keystroke = self.keyboard_input(1)
            if keystroke == CTRL_C:
                os.system('clear')
                exit()
            elif keystroke == ESCAPE_CHARACTER:
                addendum = self.keyboard_input(2)
                keystroke = keystroke + addendum
            elif keystroke.lower()=="s":
                no_input = False
                self.save()
            elif ord(keystroke) == BACKSPACE:
                print(WHITE_TEXT + "\033[{0};0H\033[K{1}\n\033[K"\
                .format(self.height + 2, MESSAGE_QUIT_EDITING))
                keystroke = self.keyboard_input(1)
                if keystroke == CTRL_C:
                    os.system('clear')
                    exit()
                elif keystroke.lower() == 'o' or keystroke.lower() == 'y':
                    self.save()
                no_input = False
                self.edit_on = False
                self.chosen = False
            elif keystroke.lower()=="c":
                no_input = False
                maze_map = self.delete_maze_walls(maze_map)
            elif keystroke.lower()=="k":
                no_input = False
                if maze_map[self.y][self.x] != LETTER_KEY:
                    maze_map[self.y][self.x] = LETTER_KEY
                elif maze_map[self.y][self.x] == LETTER_KEY:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
            elif keystroke.lower()=="d":
                no_input = False
                if maze_map[self.y][self.x] != LETTER_DOOR\
                and maze_map[self.y][self.x] != LETTER_END:
                    maze_map[self.y][self.x] = LETTER_DOOR
                elif maze_map[self.y][self.x] == LETTER_DOOR:
                    maze_map[self.y][self.x] = LETTER_END
                elif maze_map[self.y][self.x] == LETTER_END:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
            elif keystroke.lower()=="p":
                no_input = False
                if maze_map[self.y][self.x] != LETTER_PLAYER[0] \
                and maze_map[self.y][self.x] != LETTER_PLAYER[1]:
                    maze_map[self.y][self.x] = LETTER_PLAYER[0]
                elif maze_map[self.y][self.x] == LETTER_PLAYER[0]:
                    maze_map[self.y][self.x] = LETTER_PLAYER[1]
                elif maze_map[self.y][self.x] == LETTER_PLAYER[1]:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
            elif ord(keystroke) == 32:
                no_input = False
                if maze_map[self.y][self.x] != LETTER_CORRIDOR:
                    maze_map[self.y][self.x] = LETTER_CORRIDOR
                elif maze_map[self.y][self.x] == LETTER_CORRIDOR:
                    maze_map[self.y][self.x] = LETTER_WALL
            if keystroke == ARROW_DOWN and self.y < self.height - 1:
                self.y+=1
                no_input = False
            elif keystroke == ARROW_UP and self.y > 0:
                self.y-=1
                no_input = False
            elif keystroke == ARROW_LEFT and self.x > 0:
                self.x-=1
                no_input = False
            elif keystroke == ARROW_RIGHT and self.x < self.width:
                self.x+=1
                no_input = False
        groundwork_str=""
        for line in maze_map:
            for letter in line:
                groundwork_str += letter
            groundwork_str += "\n"
        self.maze = groundwork_str[:-1]

    def save(self):
        go_for_save = False
        while not go_for_save:
            maze_file = input(WHITE_TEXT + "\033[{0};0H\033[K{1}\n\033[K"\
            .format(self.height + 2, MESSAGE_SAVE_MAZE))
            maze_file = MAPS_DIRECTORY + maze_file + MAPS_FORMAT
            if os.path.exists(maze_file):
                print("\033[{0};0H\033[K{1}\n\033[K{2}".format\
                (self.height + 2, MESSAGE_SAVE_OVERWRITE_1, \
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


    def keyboard_input(self, nbl):
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        text_grab=sys.stdin.read(nbl)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        return text_grab



while True:
    editor = Editor()
    editor.maze_menu()
    while editor.edit_on:
        editor.display()
        editor.edit()
