#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

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
