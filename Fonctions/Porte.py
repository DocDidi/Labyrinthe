#! /usr/bin/env python3
# coding: utf-8

from Fonctions.var import *

class Porte:
    def __init__(self, y, x, fin = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.fin = fin
        self.bloc = False

    def __str__(self):
        if self.fin == True:
            color = RED_TEXT
            b_color = B_RED_TEXT
        else:
            color = GREEN_TEXT
            b_color = B_GREEN_TEXT
        if self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (b_color,self.y+1,self.x+1,SYMBOLEPORTE))
        elif self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (color,self.y+1,self.x+1,SYMBOLEPORTE))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLEBROUILLARD))
