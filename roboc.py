#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

chaine = ""
# for j in (RED_TEXT, GREEN_TEXT, YELLOW_TEXT,BLUE_TEXT,MAGENTA_TEXT,\
# CYAN_TEXT,WHITE_TEXT):
#     for i in range(3):
#         chaine = chaine + j + SYMBOLEMUR
#     chaine = chaine + j + SYMBOLEJOUEUR + SYMBOLEPORTE
#
# input(chaine + WHITE_TEXT)

GameOn = True
PartieEnCours = repriseSauvegarde()
while GameOn:
    # Boucle du jeu
    if PartieEnCours:
        LabyMap, PosJoueur, Fin, Portes = PartieEnCours
        PartieEnCours = False
    else:
        fichier = choixlaby()
        laby = labyload(fichier)
        LabyMap, PosJoueur, Fin, Portes = labymap(laby)

    LabyOn = True
    while LabyOn:
        afficheLaby(LabyMap)
        LabyMap, PosJoueur, Fin, Portes, LabyOn \
        = playermove(LabyMap, PosJoueur, Fin, Portes, LabyOn)
