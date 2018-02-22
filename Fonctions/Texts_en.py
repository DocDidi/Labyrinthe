#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *


MESSAGE_OS_INCOMPATIBILITY = "Sorry, \
this program is not compatible with Windows."
MESSAGE_MAP_CHOICE = "Choose your map :"
MESSAGE_MAP_LOAD = "A saved map (left/right to choose) : "
MESSAGE_MAP_CHOICE_RANDOM_SMALL = "A random map (small)"
MESSAGE_MAP_CHOICE_RANDOM_BIG = "A random map (big)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN = "A random map (console size)"
MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER = "A random map for 2 players (big)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER =\
"A random map for 2 players (console size)"
MESSAGE_MAP_CHOICE_QUIT = "Quit [Q]\n"
MESSAGE_MOVES = "\033[{}HUse arrows to move, [Q] to quit"
MESSAGE_MOVES_MULTI = "\033[{}H" + "{1}ARROWS \
{2}[I][J][K][L]".format('', COLOR_PLAYER_1, COLOR_PLAYER_2) +\
WHITE_TEXT + " [Q] to quit "
MESSAGE_WIN = "\033[{0}H\033[KCongratulations ! You escaped in {1}. \
You walked {2} steps.\n\
Press [Q] to quit, [S] to save this maze."
MESSAGE_MAP_ALREADY_SAVED = "\033[{0}H\033[KThis map is already saved."
MESSAGE_SAVE_MAZE = "Give a name to this maze : "
MESSAGE_SAVE_OVERWRITE = "This file already exists. Overwrite ?\n\
[Y] Yes, [Q] Quit, any other key to change the name."
MESSAGE_LOAD_MAZE = "There is a saved game, press [Y] to resume \
or any other key to go to the menu."
MESSAGE_ERROR_DIRECTORY = "{0} is empty or does not exists."
MESSAGE_ERROR_SCREEN_HEIGHT = "Your console is too small. \
Please expand it vertically"
MESSAGE_ERROR_SCREEN_WIDTH = "Your console is too small. \
Please expand it horizontally"
MESSAGE_SCREEN_CORRECT = "Ok ! Press [enter] to continue."
WORD_SECONDS = "seconds"
WORD_SECOND = "second"
WORD_MINUTES = "minutes"
WORD_MINUTE = "minute"
MESSAGE_HOUR_LONG = "more than an hour !"
MESSAGE_KEY = "You need to find the key."
