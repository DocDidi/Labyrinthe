#! /usr/bin/env python3
# coding: utf-8

import os

OPERATING_SYSTEM = os.name
SMALL_WIDTH = 21
SMALL_HEIGHT = 11
BIG_WIDTH = 41
BIG_HEIGHT = 21
MAPS_DIRECTORY = "Maps/"
MAPS_FORMAT = ".txt"
MAPS_LOAD = MAPS_DIRECTORY + "*" + MAPS_FORMAT
SAVE_FILE = os.environ['HOME'] + "/MazeStroller_current.save"

CTRL_C = '\x03'
ESCAPE_CHARACTER = '\x1b'
BACKSPACE = 127
ENTER = 13
SPACE = 32
ARROW_UP = '\x1b[A'
ARROW_DOWN = '\x1b[B'
ARROW_RIGHT = '\x1b[C'
ARROW_LEFT = '\x1b[D'
SYMBOL_WALL = "\U00002338"
SYMBOL_WALL_N = "\U0000257d"
SYMBOL_WALL_S = "\U0000257f"
SYMBOL_WALL_E = "\U0000257e"
SYMBOL_WALL_W = "\U0000257c"
SYMBOL_WALL_EW = "\U00002550"
SYMBOL_WALL_NS = "\U00002551"
SYMBOL_WALL_SE = "\U00002554"
SYMBOL_WALL_SW = "\U00002557"
SYMBOL_WALL_NE = "\U0000255A"
SYMBOL_WALL_NW = "\U0000255D"
SYMBOL_WALL_NSE = "\U00002560"
SYMBOL_WALL_NSW = "\U00002563"
SYMBOL_WALL_SEW = "\U00002566"
SYMBOL_WALL_NEW = "\U00002569"
SYMBOL_WALL_NSEW = "\U0000256C"
SYMBOL_DOOR = "\U0000254D"
SYMBOL_DOOR_VERTICAL = "\U0000254F"
SYMBOL_END = "\U00002505"
SYMBOL_END_VERTICAL = "\U0000250b"
SYMBOL_PLAYER = "\U0000229a"
SYMBOL_MINOTAUR = "\U0000228d"
SYMBOL_CORRIDOR = " "
SYMBOL_CORRIDOR_VISITED = "\U000022C5"
SYMBOL_FOG = "\U00002425"
SYMBOL_KEY = "\U000026b7"
BLACK_ON_WHITE = "\033[0;1;30;47m"
RED_TEXT = "\033[31m"
GREEN_TEXT = "\033[32m"
YELLOW_TEXT = "\033[33m"
BLUE_TEXT = "\033[34m"
MAGENTA_TEXT = "\033[35m"
CYAN_TEXT = "\033[36m"
WHITE_TEXT = "\033[37m"
B_RED_TEXT = "\033[1;31m"
B_GREEN_TEXT = "\033[1;32m"
B_YELLOW_TEXT = "\033[1;33m"
B_BLUE_TEXT = "\033[1;34m"
B_MAGENTA_TEXT = "\033[1;35m"
B_CYAN_TEXT = "\033[1;36m"
B_WHITE_TEXT = "\033[1;37m"
CLEAR_SCREEN = '\033[2J'
CURSOR_RESET = '\033[H'
CLR_ATTR = "\033[0m"

COLOR_PLAYER_1 = B_BLUE_TEXT
COLOR_PLAYER_2 = B_GREEN_TEXT

DEFAULT_MAP = "\
XXXXXXXXXXXXXXXXXXXXXXX\n\
X                     X\n\
X   XXX XDX XXX XXX   X\n\
X   X X X X X X X     X\n\
X   X@X XOX XXX XXX   X\n\
X   X X X X X     X   X\n\
X   XXX XXX X   XXX   X\n\
X                     X\n\
XXXXXXXXXXX_XXXXXXXXXXX\n"


OS_LANGUAGE = os.getenv('LANG')
if OS_LANGUAGE[:2] == 'fr':
    from Fonctions.Texts_fr import *
else:
    from Fonctions.Texts_en import *
