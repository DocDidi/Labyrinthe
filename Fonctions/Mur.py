#! /usr/bin/env python3
# coding: utf-8

from Fonctions.var import *

class Mur:
    def __init__(self, y, x, neighbors = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.fin = False
        self.bloc = True
        self.neighbors = neighbors

    def __str__(self):
        if self.neighbors == "N":
            SYMBOLEMUR = SYMBOLEMUR_N
        elif self.neighbors == "S":
            SYMBOLEMUR = SYMBOLEMUR_S
        elif self.neighbors == "E":
            SYMBOLEMUR = SYMBOLEMUR_E
        elif self.neighbors == "O":
            SYMBOLEMUR = SYMBOLEMUR_O
        elif self.neighbors == "EO":
            SYMBOLEMUR = SYMBOLEMUR_EO
        elif self.neighbors == "NS":
            SYMBOLEMUR = SYMBOLEMUR_NS
        elif self.neighbors == "SE":
            SYMBOLEMUR = SYMBOLEMUR_SE
        elif self.neighbors == "SO":
            SYMBOLEMUR = SYMBOLEMUR_SO
        elif self.neighbors == "NE":
            SYMBOLEMUR = SYMBOLEMUR_NE
        elif self.neighbors == "NO":
            SYMBOLEMUR = SYMBOLEMUR_NO
        elif self.neighbors == "NSE":
            SYMBOLEMUR = SYMBOLEMUR_NSE
        elif self.neighbors == "NSO":
            SYMBOLEMUR = SYMBOLEMUR_NSO
        elif self.neighbors == "SEO":
            SYMBOLEMUR = SYMBOLEMUR_SEO
        elif self.neighbors == "NEO":
            SYMBOLEMUR = SYMBOLEMUR_NEO
        elif self.neighbors == "NSEO":
            SYMBOLEMUR = SYMBOLEMUR_NSEO
        else:
            SYMBOLEMUR = "\U00002338"

        if self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (B_WHITE_TEXT,self.y+1,self.x+1,SYMBOLEMUR))
        elif self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (YELLOW_TEXT,self.y+1,self.x+1,SYMBOLEMUR))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLEBROUILLARD))
