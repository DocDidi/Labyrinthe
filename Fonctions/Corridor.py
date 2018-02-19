#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Corridor:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.revealed = False
        self.end = False
        self.block = False
        self.visited = False

    def __str__(self, *symbole):
        if self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOL_CORRIDOR))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOL_FOG))
