#! /usr/bin/env python3
# coding: utf-8

import time

from Fonctions.Fonctions import *
from Fonctions.Variables import *

if OPERATING_SYSTEM == 'nt':
    print(MESSAGE_OS_INCOMPATIBILITY)
    exit()

GameOn = True
ongoing_game = load_file()
maze_menu_obj = StartMenu()

while GameOn:
    if ongoing_game:
        game_screen = ongoing_game
        ongoing_game = False
    else:
        maze = maze_menu(maze_menu_obj)
        game_screen = GameScreen(maze)
    game_screen.start()
    while game_screen.maze_on:
        game_screen.display()
        player_move(game_screen, maze_menu_obj)
        for item in game_screen.props:
            if game_screen.player_have_key and item.end:
                item.block = False
            if item.has_key:
                for player in game_screen.players:
                    if (player.x, player.y) == (item.x, item.y):
                        item.has_key = False
                        game_screen.player_have_key = True
            if item.end:
                for player in game_screen.players:
                    if (player.x, player.y) == (item.x, item.y):
                        game_screen.maze_on = False
                        game_screen.finished_menu(maze_menu_obj)
