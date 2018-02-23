#! /usr/bin/env python3
# coding: utf-8

import glob
from Fonctions.Variables import *
from Fonctions.GenerateMaze import *

class StartMenu():
    def __init__(self):
        self.selected = 0
        self.chosen = False
        self.file_index = 0
        self.choice = []
        self.file_path = MAPS_LOAD.find("*")
        self.directory_content = glob.glob(MAPS_LOAD)
        self.min_choice = 0
        if not self.directory_content:
            self.saved_maps = (MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY))
            self.selected = 1
            self.min_choice = 1
        else:
            self.saved_maps = MESSAGE_MAP_LOAD+self.directory_content\
            [self.file_index][self.file_path:-4].capitalize()


    def __str__(self):
        if not self.directory_content:
            self.saved_maps = \
            (B_RED_TEXT + MESSAGE_ERROR_DIRECTORY.format(MAPS_DIRECTORY))
        else:
            self.saved_maps = \
            MESSAGE_MAP_LOAD+self.directory_content\
            [self.file_index][self.file_path:-4].capitalize()
        self.choice = [self.saved_maps] + [MESSAGE_MAP_CHOICE_RANDOM_SMALL,\
        MESSAGE_MAP_CHOICE_RANDOM_BIG,\
        MESSAGE_MAP_CHOICE_RANDOM_SCREEN,\
        MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER,\
        MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER,\
        MESSAGE_MAP_CHOICE_QUIT]
        result_str = ""
        for i, maze_map in enumerate(self.choice):
            if i == self.selected:
                result_str += \
                BLACK_ON_WHITE + maze_map + WHITE_TEXT
            else:
                if maze_map == MESSAGE_MAP_CHOICE_QUIT:
                    result_str += B_RED_TEXT + maze_map
                else:
                    result_str += WHITE_TEXT + maze_map
            result_str += "\n"
        return result_str

    def getmap(self):
        if self.chosen == self.saved_maps and self.directory_content:
            self.chosen =\
            self.directory_content[self.file_index]
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
            exit()
