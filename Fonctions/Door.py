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

    def __str__(self):
        if self.end == True:
            color = RED_TEXT
            b_color = B_RED_TEXT
        elif self.visited == True:
            color = MAGENTA_TEXT
            b_color = B_MAGENTA_TEXT
        else:
            color = GREEN_TEXT
            b_color = B_GREEN_TEXT
        if self.vertical == True :
            symbol = SYMBOL_DOOR_VERTICAL
        else :
            symbol = SYMBOL_DOOR


        if self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (b_color,self.y+1,self.x+1,symbol))
        elif self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (color,self.y+1,self.x+1,symbol))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOL_FOG))
