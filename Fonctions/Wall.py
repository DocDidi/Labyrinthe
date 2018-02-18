#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Var import *

class Wall:
    def __init__(self, y, x, neighbors = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.end = False
        self.block = True
        self.neighbors = neighbors

    def __str__(self):
        if self.neighbors == "N":
            SYMBOL_WALL = SYMBOL_WALL_N
        elif self.neighbors == "S":
            SYMBOL_WALL = SYMBOL_WALL_S
        elif self.neighbors == "E":
            SYMBOL_WALL = SYMBOL_WALL_E
        elif self.neighbors == "O":
            SYMBOL_WALL = SYMBOL_WALL_W
        elif self.neighbors == "EO":
            SYMBOL_WALL = SYMBOL_WALL_EW
        elif self.neighbors == "NS":
            SYMBOL_WALL = SYMBOL_WALL_NS
        elif self.neighbors == "SE":
            SYMBOL_WALL = SYMBOL_WALL_SE
        elif self.neighbors == "SO":
            SYMBOL_WALL = SYMBOL_WALL_SW
        elif self.neighbors == "NE":
            SYMBOL_WALL = SYMBOL_WALL_NE
        elif self.neighbors == "NO":
            SYMBOL_WALL = SYMBOL_WALL_NW
        elif self.neighbors == "NSE":
            SYMBOL_WALL = SYMBOL_WALL_NSE
        elif self.neighbors == "NSO":
            SYMBOL_WALL = SYMBOL_WALL_NSW
        elif self.neighbors == "SEO":
            SYMBOL_WALL = SYMBOL_WALL_SEW
        elif self.neighbors == "NEO":
            SYMBOL_WALL = SYMBOL_WALL_NEW
        elif self.neighbors == "NSEO":
            SYMBOL_WALL = SYMBOL_WALL_NSEW
        else:
            SYMBOL_WALL = "\U00002338"

        if self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (B_WHITE_TEXT,self.y+1,self.x+1,SYMBOL_WALL))
        elif self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (YELLOW_TEXT,self.y+1,self.x+1,SYMBOL_WALL))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOL_FOG))
