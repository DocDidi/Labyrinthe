#! /usr/bin/env python3
# coding: utf-8

from Fonctions.var import *

class Couloir:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.revealed = False
        self.fin = False
        self.bloc = False

    def __str__(self):
        if self.revealed == True:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLECOULOIR))
        else:
            return ("{0}\033[{1};{2}H{3}".format\
            (WHITE_TEXT,self.y+1,self.x+1,SYMBOLEBROUILLARD))
