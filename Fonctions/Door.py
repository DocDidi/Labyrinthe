#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Door:
    def __init__(self, y, x, vertical, end = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.end = end
        self.block = end
        self.vertical = vertical
        self.visited = False
        self.has_key = False
        self.sight = False

    def __str__(self):
        if self.end == True:
            color = RED_TEXT
            b_color = B_RED_TEXT
        elif self.visited == True:
            color = MAGENTA_TEXT
            b_color = B_MAGENTA_TEXT
        else:
            color = YELLOW_TEXT
            b_color = B_WHITE_TEXT
        if self.vertical == True :
            symbol = SYMBOL_DOOR_VERTICAL
        else :
            symbol = SYMBOL_DOOR
        if self.lit:
            color = b_color
        if not self.revealed:
            color = WHITE_TEXT
            symbol = SYMBOL_FOG

        if self.lit:
            return color+symbol+CLR_ATTR
        else:
            return color+symbol

    def display(self, margin, margin_v):
        print("\033[{0};{1}H{2}".format\
        (self.y+margin_v,self.x+1+margin,str(self)))
