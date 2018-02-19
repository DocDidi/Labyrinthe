#! /usr/bin/env python3
# coding: utf-8

from Fonctions.Variables import *

class Player:
    def __init__(self, y, x):
        self.x = x
        self.y = y

    def __str__(self):
        return ("{0}\033[{1};{2}H{3}".format\
        (B_BLUE_TEXT,self.y+1,self.x+1,SYMBOL_PLAYER))

    # def Posplayer(self):
    #     return [self.y,self.x]
