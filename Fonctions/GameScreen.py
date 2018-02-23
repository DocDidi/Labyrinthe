#! /usr/bin/env python3
# coding: utf-8

import os
from Fonctions.Variables import *
from Fonctions.Variables_Map_Building import *
from Fonctions.Player import *
from Fonctions.Wall import *
from Fonctions.Door import *
from Fonctions.Corridor import *


class GameScreen:

    def __init__(self, maze):
        """Extrait les données du jeu de la carte (str)"""
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
                    players.append(Player(i,j))
                    props.append(Corridor(i,j))
                    check_player = True
                if letter is LETTER_PLAYER[1]:
                    players.append(Player(i,j,player_number = 2))
                    props.append(Corridor(i,j))
                elif letter is LETTER_END:
                    vertical = False
                    if j == 0 or j == len(line)-1:
                        vertical = True
                    props.append(Door(i,j,vertical,end = True))
                    check_end = True
                elif letter is LETTER_DOOR:
                    vertical = False
                    if lines[i][j+1] == LETTER_CORRIDOR\
                    or lines[i][j-1] == LETTER_CORRIDOR:
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
                    check_key = True
                else:
                    props.append(Corridor(i,j))
        if check_player and check_end and check_key:
            self.players = players
            self.props = props
            self.height = i
            self.width = j
            self.maze = maze
        else:
            self.__init__(DEFAULT_MAP)

        self.player_have_key = False
        self.maze_on = True

    def display(self):
        self.check_screen_size()
        for item in self.props:
            item.lit = False
            for player in self.players:
                if ((-2 <= player.x - item.x <= 2) \
                and (-3 <= player.y - item.y <= 3))\
                or ((-3 <= player.x - item.x <= 3) \
                and (-2 <= player.y - item.y <= 2)):
                    item.revealed = True
                if ((-1 <= player.x - item.x <= 1) \
                and (-2 <= player.y - item.y <= 2))\
                or ((-2 <= player.x - item.x <= 2) \
                and (-1 <= player.y - item.y <= 1)):
                    item.lit = True
                if player.x == item.x and player.y == item.y:
                    item.visited = True
        maze_map = ""
        for item in self.props:
            maze_map = maze_map + str(item)
        print(CLEAR_SCREEN + maze_map)
        for player in self.players:
            print(player)
        if self.player_have_key:
            print(WHITE_TEXT + "\033[{0}H{1}\033[1B"\
            .format(self.height + 1, SYMBOL_KEY))
        else:
            print(WHITE_TEXT + "\033[{0}H{1}\033[1B"\
            .format(self.height + 1, MESSAGE_KEY))
        if len(self.players)>1:
            print(MESSAGE_MOVES_MULTI.format(self.height + 2))
        else:
            print(WHITE_TEXT + MESSAGE_MOVES.format(self.height + 2))

    def check_screen_size(self):
        """Demande à l'utilisateur d'agrandir sa console si besoin."""
        CORRECT_HEIGHT = True
        CORRECT_WIDTH = True
        rows, columns = os.popen('stty size', 'r').read().split()
        while int(rows) < self.height + 3:
            CORRECT_HEIGHT = False
            rows, columns = os.popen('stty size', 'r').read().split()
            print(CLEAR_SCREEN + MESSAGE_ERROR_SCREEN_HEIGHT)
        if CORRECT_HEIGHT == False:
            print(CLEAR_SCREEN + MESSAGE_SCREEN_CORRECT)
            input()
        while int(columns) < self.width:
            CORRECT_WIDTH = False
            rows, columns = os.popen('stty size', 'r').read().split()
            print(CLEAR_SCREEN + MESSAGE_ERROR_SCREEN_WIDTH)
        if CORRECT_WIDTH == False:
            print(CLEAR_SCREEN + MESSAGE_SCREEN_CORRECT)
            input()
