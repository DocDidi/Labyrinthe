#! /usr/bin/env python3
# coding: utf-8

from fonctionsRoboc import *

from var import *

GameOn = True
PartieEnCours = repriseSauvegarde()
while GameOn:
    # Boucle du jeu
    if PartieEnCours:
        LabyMap, Joueur, Fin, Portes = PartieEnCours
        PartieEnCours = False
    else:
        fichier = choixlaby()
        laby = labyload(fichier)
        LabyMap, Joueur, Fin, Portes = labymap(laby)
        input((LabyMap, Joueur, Fin, Portes))

    LabyOn = True
    while LabyOn:
        afficheLaby(LabyMap, Joueur)
        LabyMap, Fin, Portes, LabyOn \
        = playermove(LabyMap, Joueur, Fin, Portes, LabyOn)
