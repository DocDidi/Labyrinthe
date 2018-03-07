#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

KEY_UP_PLAYER_2 = 'w'
KEY_DOWN_PLAYER_2 = 's'
KEY_LEFT_PLAYER_2 = 'a'
KEY_RIGHT_PLAYER_2 = 'd'


MESSAGE_OS_INCOMPATIBILITY = "Sorry, \
this program is not compatible with Windows."
MESSAGE_MAP_CHOICE = "Choose your map :"
MESSAGE_MAP_LOAD = "A saved map (left/right to choose) : "
MESSAGE_MAP_CHOICE_RANDOM_SMALL = "A random map (small)"
MESSAGE_MAP_CHOICE_RANDOM_BIG = "A random map (big)"
MESSAGE_MAP_CHOICE_DEFINE_SIZE = "A random map (you choose the size)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN = "A random map (console size)"
MESSAGE_SET_SIZE = "A random map of size : {0} x {1} [Space] to change size."
MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER = "A random map for 2 players (big)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER =\
"A random map for 2 players (console size)"
MESSAGE_MAP_CHOICE_QUIT = "Quit [Backspace]\n"
MESSAGE_MOVES = "Use arrows to move, [Backspace] to quit"
MESSAGE_MOVES_MULTI = "{0}Arrows {1}[Z][Q][S][D] \
{2}[Backspace] to quit ".format(COLOR_PLAYER_1, COLOR_PLAYER_2, WHITE_TEXT)
MESSAGE_WIN_1 = "Congratulations ! You escaped in {0}. \
You walked {1} steps."
MESSAGE_WIN_2 = "Press [Backspace] to quit, [K] to save this maze, \
[ENTER] to play again."
MESSAGE_WIN_2_SAVED = "Press [Backspace] to quit."
MESSAGE_MAP_ALREADY_SAVED = "This map is already saved."
MESSAGE_SAVE_MAZE = "Give a name to this maze : "
MESSAGE_SAVE_OVERWRITE_1 = "This file already exists. Overwrite ?"
MESSAGE_SAVE_OVERWRITE_2 = "[Y] Yes, [Backspace] Quit, \
any other key to change the name."
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
MESSAGE_HOUR_LONG = "more than an hour"
MESSAGE_KEY = "You need to find the key."
MESSAGE_WIDTH = "Width : "
MESSAGE_HEIGHT = "Height : "
MESSAGE_EDITOR_KEYS = "[Space]Walls [D]Doors/End [P]Player 1/2 [K]Key \
[Backspace]Erase all [S]Save"
MESSAGE_DIFFICULTY = ["< Easy >","< Normal >","< Hard >"]
MESSAGE_DIFFICULTY_COLORS = [B_GREEN_TEXT,B_YELLOW_TEXT,B_RED_TEXT]
MESSAGE_NUMBER_PLAYERS = ["< One player >", "< Two players >"]
MESSAGE_CONTROLS_SIZE = "Arrows to resize"
