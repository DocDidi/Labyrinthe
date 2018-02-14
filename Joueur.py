#! /usr/bin/env python3
# coding: utf-8

from var import *
from Joueur import *

class Personnage:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return ("{0}\033[{1};{2}H{3}".format\
        (BLUE_TEXT,self.y+1,self.x+1,SYMBOLEJOUEUR))

    def PosJoueur(self):
        return [self.y,self.x]
