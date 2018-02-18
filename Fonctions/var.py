#! /usr/bin/env python3
# coding: utf-8

import os

LETTREMURS = "X"
LETTREJOUEUR = "O"
LETTREFIN = "_"
LETTREPORTE = "#"
LETTRECOULOIR = " "
CTRL_C = '\x03'
ECHAP_CARAC = '\x1b'
FLECHE_HAUT = '\x1b[A'
FLECHE_BAS = '\x1b[B'
FLECHE_DROITE = '\x1b[C'
FLECHE_GAUCHE = '\x1b[D'
EFFACE_ECRAN = '\033[2J'
RESET_CURSEUR = '\033[H'

SYSTEME_D_EXPLOITATION = os.name
MESSAGEINCOMPATIBILITESYSTEME = "Désolé, \
ce programme n'est pas compatible avec Windows."

FICHIERDESAUVEGARDE = os.environ['HOME']+"/LabyrintheEnCours.save"
SYMBOLEMUR = "\U00002338"
SYMBOLEPORTE = "\U000022c2"
SYMBOLEJOUEUR = "\U0000229b"
SYMBOLECOULOIR = " "
SYMBOLECOULOIRVISITE = "\U000022C5"
SYMBOLEBROUILLARD = "\U0000223F"
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

EMPLACEMENTCARTES = "Cartes/"
FORMATCARTE = ".txt"
CHARGEMENTCARTES = EMPLACEMENTCARTES + "*" + FORMATCARTE


MESSAGECHOIXCARTE = "Quelle carte voulez-vous jouer ?"
MESSAGECARTEPREDEFINIE = "Une carte prédéfinie \
(gauche et droite pour choisir) : "
MESSAGECHOIXCARTEALEATOIREPETITE = "Une carte aléatoire (petite)"
LARGEURPETITE = 21
HAUTEURPETITE = 11
MESSAGECHOIXCARTEALEATOIREGRANDE = "Une carte aléatoire (grande)"
LARGEURGRANDE = 41
HAUTEURGRANDE = 21
MESSAGECHOIXCARTEALEATOIREECRAN = "Une carte aléatoire \
(de la taille de la console)"
MESSAGECHOIXQUITTER = "Quitter [Q]\n"
MESSAGEDEMANDEMOUVEMENT = "\033[{}HTouches flechées pour \
vous déplacer. [Q] pour quitter "
MESSAGEREUSSITELABY = "\033[{0}H\033[KBravo ! Vous avez fini en {1}.\n\
(pressez [Q] pour revenir au menu, [S] pour sauvegarder ce labyrinthe.)"
MESSAGESAUVEGARDELABYRINTHE = "Quel nom voulez vous donner à ce labyrinthe ? "
MESSAGEREPRISESAUVEGARDE = "Il y a une partie sauvegardée,\
 pressez [O] pour la continuer."
MESSAGEERREURDOSSIER = "Le répertoire {0} est vide ou n'existe pas."
MESSAGEERREURCHOIXCARTE = "Désolé, votre choix est invalide."
MESSAGEERREURMOUVEMENT = "Mauvaise direction."
MESSAGEHAUTEURECRANINCORRECT = "Votre console est trop petite. \
Veuillez l'agrandir verticalement."
MESSAGELARGEURECRANINCORRECT = "Votre console est trop petite. \
Veuillez l'agrandir horizontalement."
MESSAGEECRANCORRECT = "C'est bon ! Pressez entrée pour continuer."
CARTEDEFAUT = "\
XXXXXXXXXXXXXXXXXXXXXXX\n\
X                     X\n\
X   XXX X X XXX XXX   X\n\
X   X X X X X X X     X\n\
X   X_X XOX XXX XXX   X\n\
X   X X X X X     X   X\n\
X   XXX XXX X   XXX   X\n\
X                     X\n\
XXXXXXXXXXXXXXXXXXXXXXX\n"
