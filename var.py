#! /usb/bin/env python3
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
if SYSTEME_D_EXPLOITATION == 'nt':
    FICHIERDESAUVEGARDE = "LabyrintheEnCours.save"
    SYMBOLEMUR = "X"
    SYMBOLEPORTE = "#"
    SYMBOLEFIN = " "
    SYMBOLEJOUEUR = "O"
    RED_TEXT = ""
    GREEN_TEXT = ""
    YELLOW_TEXT = ""
    BLUE_TEXT = ""
    MAGENTA_TEXT = ""
    CYAN_TEXT = ""
    WHITE_TEXT = ""

else:
    FICHIERDESAUVEGARDE = os.environ['HOME']+"/LabyrintheEnCours.save"
    SYMBOLEMUR = "\U00002338"
    SYMBOLEPORTE = "\U000022c2"
    SYMBOLEFIN = " "
    SYMBOLEJOUEUR = "\U0000229b"
    RED_TEXT = "\033[31m"
    GREEN_TEXT = "\033[32m"
    YELLOW_TEXT = "\033[33m"
    BLUE_TEXT = "\033[34m"
    MAGENTA_TEXT = "\033[35m"
    CYAN_TEXT = "\033[36m"
    WHITE_TEXT = "\033[37m"

EMPLACEMENTCARTES = "Cartes/*.txt"

MESSAGECHOIXCARTE = "Quelle carte voulez-vous jouer ?"
MESSAGEDEMANDEMOUVEMENT = "Utilisez les touches flechées pour vous déplacer.\
 (Q pour quitter) "
# MESSAGEDEMANDEMOUVEMENT = "Ou allez vous ? (N/S/E/O)(Q pour quitter) "
MESSAGEREUSSITELABY = "Bravo ! (pressez une touche pour revenir au menu)"
MESSAGEREPRISESAUVEGARDE = "Il y a une partie sauvegardée,\
 voulez vous la continuer ?"
MESSAGEERREURDOSSIER = "Le répertoirre {0} est vide ou n'existe pas."
MESSAGEERREURCHOIXCARTE = "Désolé, votre choix est invalide."
MESSAGEERREURMOUVEMENT = "Mauvaise direction."
MESSAGEECHECCHOIXCARTE = "Désolé, Au revoir."
CARTEDEFAUT = "XXXXX X   X XXXXX XXXXX\nX   X X   X X _ X X\
\nX O X X   X XXXXX XXXXX\nX   X X   X X         X\nXXXXX XXXXX X     XXXXX\n\n\
La carte que vous avez chargée n'est pas valide."
