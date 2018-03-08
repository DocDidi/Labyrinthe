#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

KEY_UP_PLAYER_2 = 'z'
KEY_DOWN_PLAYER_2 = 's'
KEY_LEFT_PLAYER_2 = 'q'
KEY_RIGHT_PLAYER_2 = 'd'

# --START MENU--

MESSAGE_OS_INCOMPATIBILITY = "Désolé, \
ce programme n'est pas compatible avec Windows."
MESSAGE_LOAD_MAZE = "Il y a une partie sauvegardée,\
 pressez [O] pour la continuer."
MESSAGE_ERROR_DIRECTORY = "Le répertoire {0} est vide ou n'existe pas."
MESSAGE_MAP_CHOICE = "Quelle carte voulez-vous jouer ?"
MESSAGE_MAP_LOAD = "Une carte prédéfinie (gauche et droite pour choisir) : "
MESSAGE_MAP_CHOICE_RANDOM_SMALL = "Une carte aléatoire (petite)"
MESSAGE_MAP_CHOICE_RANDOM_BIG = "Une carte aléatoire (grande)"
MESSAGE_MAP_CHOICE_DEFINE_SIZE = "Une carte aléatoire (choix de la taille)"
MESSAGE_MAP_CHOICE_RANDOM_SCREEN = "Une carte aléatoire \
(de la taille de la console)"
MESSAGE_SET_SIZE = "Une carte de taille : {0} x {1} \
[Espace] pour redimensionner."
# MESSAGE_MAP_CHOICE_RANDOM_BIG_MULTIPLAYER =\
# "Une carte aléatoire (grande) 2 JOUEURS"
# MESSAGE_MAP_CHOICE_RANDOM_SCREEN_MULTIPLAYER =\
# "Une carte aléatoire (de la taille de la console) 2 JOUEURS"
MESSAGE_DIFFICULTY = ["< Facile >","< Normal >","< Difficile >"]
MESSAGE_DIFFICULTY_COLORS = [B_GREEN_TEXT,B_YELLOW_TEXT,B_RED_TEXT]
MESSAGE_NUMBER_PLAYERS = ["< Un joueur >", "< Deux joueurs >"]
MESSAGE_CONTROLS_SIZE = "Touches flechées pour redimensionner"
MESSAGE_MAP_CHOICE_QUIT = "Quitter [Ret.Arr.]\n"

# --GAME SCREEN--

MESSAGE_MOVES = "Touches flechées pour \
vous déplacer. [Ret.Arr] pour quitter "
MESSAGE_MOVES_MULTI = "{0}Touches flechées {1}[Z][Q][S][D] \
{2}[Ret.Arr] pour quitter ".format(COLOR_PLAYER_1, COLOR_PLAYER_2, WHITE_TEXT)
MESSAGE_WIN_1 = "Bravo ! Vous avez fini en {0}. Vous avez fait {1} pas."
MESSAGE_WIN_2 = "pressez [Ret.Arr] pour revenir au menu, \
[K] pour sauvegarder ce labyrinthe, [ENTREE] pour rejouer."
MESSAGE_WIN_2_SAVED = "pressez [Ret.Arr] pour revenir au menu."
MESSAGE_MAP_ALREADY_SAVED = "Cette carte est déjà sauvegardée."
MESSAGE_SAVE_MAZE = "Quel nom voulez vous donner à ce labyrinthe ? "
MESSAGE_SAVE_OVERWRITE_1 = "Ce fichier existe. L'écraser ?"
MESSAGE_SAVE_OVERWRITE_2 = "[O] Oui, [Ret.Arr] Quitter, \
Une autre touche pour renommer."
MESSAGE_ERROR_SCREEN_HEIGHT = "Votre console est trop petite. \
Veuillez l'agrandir verticalement."
MESSAGE_ERROR_SCREEN_WIDTH = "Votre console est trop petite. \
Veuillez l'agrandir horizontalement."
MESSAGE_SCREEN_CORRECT = "C'est bon ! Pressez entrée pour continuer."
WORD_SECONDS = "secondes"
WORD_SECOND = "seconde"
WORD_MINUTES = "minutes"
WORD_MINUTE = "minute"
MESSAGE_HOUR_LONG = "plus d'une heure"
MESSAGE_KEY = "Vous devez trouver la clé."

# --EDITOR--

MESSAGE_WIDTH = "Largeur : "
MESSAGE_HEIGHT = "Hauteur : "
MESSAGE_EDITOR_KEYS = "[Espace]Murs [D]Portes/fin [P]Joueur 1/2 [K]Clé\n\
[C]Effacer tout [S]Sauvegarde [Ret.Arr.]Quitter"
MESSAGE_DELETE_MAZE_WALLS = "Voulez-vous vider ce labyrinthe ? [O]"
MESSAGE_QUIT_EDITING = "Voulez-vous sauvegarder ? [O]"
