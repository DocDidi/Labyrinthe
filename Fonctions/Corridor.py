#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Corridor:
    def __init__(self, y, x, has_key = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.end = False
        self.block = False
        self.visited = False
        self.has_key = has_key
        self.sight = True

    def __str__(self):
        color = WHITE_TEXT
        symbol = SYMBOL_CORRIDOR
        if self.has_key:
            color = B_WHITE_TEXT
            symbol = SYMBOL_KEY
        if not self.revealed:
            color = WHITE_TEXT
            symbol = SYMBOL_FOG

        return color+symbol+CLR_ATTR
