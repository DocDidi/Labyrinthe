#! /usr/bin/env python3
# coding: utf-8

from var import *

class Porte:
    def __init__(self, y, x, fin = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False
        self.fin = fin
        self.bloc = False

    def __str__(self):
        if self.revealed == True and self.lit == False:
            return ("{0}\033[{1};{2}H{3}".format\
            (GREEN_TEXT,self.y+1,self.x+1,SYMBOLEPORTE))
        elif self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (B_GREEN_TEXT,self.y+1,self.x+1,SYMBOLEPORTE))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLEBROUILLARD))