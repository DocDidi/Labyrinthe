#! /usr/bin/env python3
# coding: utf-8

from var import *

class Mur:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.revealed = False
        self.lit = False

    def __str__(self):
        if self.revealed == True and self.lit == False:
            return ("{0}\033[{1};{2}H{3}".format\
            (YELLOW_TEXT,self.y+1,self.x+1,SYMBOLEMUR))
        elif self.lit == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (B_YELLOW_TEXT,self.y+1,self.x+1,SYMBOLEMUR))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLEBROUILLARD))
