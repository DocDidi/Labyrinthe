#! /usb/bin/env python3

LETTREMURS = "X"
LETTREJOUEUR = "O"
LETTREFIN = "_"
LETTREPORTE = "#"
LETTRECOULOIR = " "

FICHIERDESAUVEGARDE = "PartieEnCours"
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
SYMBOLEMUR = "\U00002338"
SYMBOLEPORTE = "\U000022c2"
SYMBOLEFIN = " "
SYMBOLEJOUEUR = "\U0000229b"
CTRL_C = '\x03'
ECHAP_CARAC = '\x1b'
FLECHE_HAUT = '\x1b[A'
FLECHE_BAS = '\x1b[B'
FLECHE_DROITE = '\x1b[C'
FLECHE_GAUCHE = '\x1b[D'
EFFACE_ECRAN = '\033[2J'
RESET_CURSEUR = '\033[H'
