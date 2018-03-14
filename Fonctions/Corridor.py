#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *


class Corridor:
    def __init__(self, y, x, has_key=False):
        self.x = x
        self.y = y
        self.revealed = False
        self.end = False
        self.block = False
        self.visited = False
        self.has_key = has_key
        self.sight = True
        self.lit = False

    def __str__(self):
        color = WHITE_TEXT
        symbol = SYMBOL_CORRIDOR
        if self.has_key:
            color = B_WHITE_TEXT
            symbol = SYMBOL_KEY
        if not self.revealed:
            color = WHITE_TEXT
            symbol = SYMBOL_FOG

        if self.lit or self.has_key:
            return color+symbol+CLR_ATTR
        else:
            return color+symbol

    def display(self, margin, margin_v):
        print(
            "\033[{0};{1}H{2}"
            .format(self.y+margin_v, self.x + 1 + margin, str(self)))
