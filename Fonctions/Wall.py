#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Wall:
    def __init__(self, y, x, neighbors = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.end = False
        self.block = True
        self.neighbors = neighbors
        self.has_key = False
        if self.neighbors == "N":
            self.symbol = SYMBOL_WALL_N
        elif self.neighbors == "S":
            self.symbol = SYMBOL_WALL_S
        elif self.neighbors == "E":
            self.symbol = SYMBOL_WALL_E
        elif self.neighbors == "W":
            self.symbol = SYMBOL_WALL_W
        elif self.neighbors == "EW":
            self.symbol = SYMBOL_WALL_EW
        elif self.neighbors == "NS":
            self.symbol = SYMBOL_WALL_NS
        elif self.neighbors == "SE":
            self.symbol = SYMBOL_WALL_SE
        elif self.neighbors == "SW":
            self.symbol = SYMBOL_WALL_SW
        elif self.neighbors == "NE":
            self.symbol = SYMBOL_WALL_NE
        elif self.neighbors == "NW":
            self.symbol = SYMBOL_WALL_NW
        elif self.neighbors == "NSE":
            self.symbol = SYMBOL_WALL_NSE
        elif self.neighbors == "NSW":
            self.symbol = SYMBOL_WALL_NSW
        elif self.neighbors == "SEW":
            self.symbol = SYMBOL_WALL_SEW
        elif self.neighbors == "NEW":
            self.symbol = SYMBOL_WALL_NEW
        elif self.neighbors == "NSEW":
            self.symbol = SYMBOL_WALL_NSEW
        else:
            self.symbol = SYMBOL_WALL



    def __str__(self):
        if self.lit:
            color = B_WHITE_TEXT
        else:
            color = YELLOW_TEXT

        if self.revealed:
            symbol = self.symbol
        else:
            color = WHITE_TEXT
            symbol = SYMBOL_FOG

        return ("{0}\033[{1};{2}H{3}".format\
        (color,self.y+1,self.x+1,symbol))
