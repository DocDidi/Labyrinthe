#! /usr/bin/env python3
# coding: utf-8

import os

OS_LANGUAGE = os.getenv('LANG')
OPERATING_SYSTEM = os.name
SMALL_WIDTH = 21
SMALL_HEIGHT = 11
BIG_WIDTH = 41
BIG_HEIGHT = 21
MAPS_DIRECTORY = "Cartes/"
MAPS_FORMAT = ".txt"
MAPS_LOAD = MAPS_DIRECTORY + "*" + MAPS_FORMAT
SAVE_FILE = os.environ['HOME']+"/MazeStroller_current.save"

LETTER_WALL = "X"
LETTER_PLAYER = "OI" #Player1 = O, player2 = I
LETTER_END = "_"
LETTER_DOOR = "#"
LETTER_CORRIDOR = " "
LETTER_KEY = "@"
CTRL_C = '\x03'
ESCAPE_CHARACTER = '\x1b'
ARROW_UP = '\x1b[A'
ARROW_DOWN = '\x1b[B'
ARROW_RIGHT = '\x1b[C'
ARROW_LEFT = '\x1b[D'
CLEAR_SCREEN = '\033[2J'
CURSOR_RESET = '\033[H'
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
SYMBOL_DOOR = "\U00002504"
SYMBOL_DOOR_VERTICAL = "\U0000250A"
SYMBOL_PLAYER = "\U0000229a"
SYMBOL_CORRIDOR = " "
SYMBOL_CORRIDOR_VISITED = "\U000022C5"
SYMBOL_FOG = "\U00002425"
SYMBOL_KEY = "\U000026b7"
BLACK_ON_WHITE = "\033[0;1;30;47m"
RED_TEXT = "\033[0;31m"
GREEN_TEXT = "\033[0;32m"
YELLOW_TEXT = "\033[0;33m"
BLUE_TEXT = "\033[0;34m"
MAGENTA_TEXT = "\033[0;35m"
CYAN_TEXT = "\033[0;36m"
WHITE_TEXT = "\033[0;37m"
B_RED_TEXT = "\033[0;1;31m"
B_GREEN_TEXT = "\033[0;1;32m"
B_YELLOW_TEXT = "\033[0;1;33m"
B_BLUE_TEXT = "\033[0;1;34m"
B_MAGENTA_TEXT = "\033[0;1;35m"
B_CYAN_TEXT = "\033[0;1;36m"
B_WHITE_TEXT = "\033[0;1;37m"

COLOR_PLAYER_1 = B_BLUE_TEXT
COLOR_PLAYER_2 = B_RED_TEXT

MESSAGE_OS_INCOMPATIBILITY = "Désolé, \
ce programme n'est pas compatible avec Windows."
MESSAGE_MAP_CHOICE = "Quelle carte voulez-vous jouer ?"
MESSAGE_MAP_LOAD = "Une carte prédéfinie \
(gauche et droite pour choisir) : "
MESSAGE_MAP_CHOICE_RANDOM_SMALL = "Une carte aléatoire (petite)"
MESSAGE_MAP_CHOICE_RANDOM_BIG = "Une carte aléatoire (grande)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN = "Une carte aléatoire \
(de la taille de la console)"
MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER =\
"Une carte aléatoire (grande) 2 JOUEURS"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER =\
"Une carte aléatoire (de la taille de la console) 2 JOUEURS"
MESSAGE_MAP_CHOICE_QUIT = "Quitter [Q]\n"
MESSAGE_MOVES = "\033[{}HTouches flechées pour \
vous déplacer. [Q] pour quitter "
MESSAGE_MOVES_MULTI = "\033[{}H" + "{1}Touches flechées \
{2}[I][J][K][L]".format('', COLOR_PLAYER_1, COLOR_PLAYER_2) +\
WHITE_TEXT + " [Q] pour quitter "
MESSAGE_WIN = "\033[{0}H\033[KBravo ! \
Vous avez fini en {1}. Vous avez fait {2} pas.\n\
(pressez [Q] pour revenir au menu, [S] pour sauvegarder ce labyrinthe.)"
MESSAGE_SAVE_MAZE = "Quel nom voulez vous donner à ce labyrinthe ? "
MESSAGE_LOAD_MAZE = "Il y a une partie sauvegardée,\
 pressez [O] pour la continuer."
MESSAGE_ERROR_DIRECTORY = "Le répertoire {0} est vide ou n'existe pas."
MESSAGE_ERROR_SCREEN_HEIGHT = "Votre console est trop petite. \
Veuillez l'agrandir verticalement."
MESSAGE_ERROR_SCREEN_WIDTH = "Votre console est trop petite. \
Veuillez l'agrandir horizontalement."
MESSAGE_SCREEN_CORRECT = "C'est bon ! Pressez entrée pour continuer."
WORD_SECONDS = "secondes"
WORD_SECOND = "seconde"
WORD_MINUTES = "minutes"
WORD_MINUTE = "minute"
MESSAGE_HOUR_LONG = "plus d'une heure !"

DEFAULT_MAP = "\
XXXXXXXXXXXXXXXXXXXXXXX\n\
X                     X\n\
X   XXX X X XXX XXX   X\n\
X   X X X X X X X     X\n\
X   X_X XOX XXX XXX   X\n\
X   X X X X X     X   X\n\
X   XXX XXX X   XXX   X\n\
X                     X\n\
XXXXXXXXXXXXXXXXXXXXXXX\n"
