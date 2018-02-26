#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Fonctions import *
from Fonctions.Variables import *
from Fonctions.StartMenu import *
from Fonctions.GameScreen import *

if OPERATING_SYSTEM == 'nt':
    print(MESSAGE_OS_INCOMPATIBILITY)
    exit()

ongoing_game = load_file()
start_menu = StartMenu()

while True:
    if ongoing_game:
        game_screen = ongoing_game
        ongoing_game = False
    else:
        maze = start_menu.maze_menu()
        game_screen = GameScreen(maze, start_menu)
    game_screen.start()
    while game_screen.maze_on:
        game_screen.display()
        game_screen.player_move()
        game_screen.tests()
