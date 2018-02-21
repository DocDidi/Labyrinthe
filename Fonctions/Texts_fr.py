#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *


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
pressez [Q] pour revenir au menu, [S] pour sauvegarder ce labyrinthe."
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
MESSAGE_KEY = "Vous devez trouver la clé."
