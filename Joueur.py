#! /usr/bin/env python3
# coding: utf-8

class Joueur:
    def __init__(self, y, x):
        x = self.x
        y = self.y

    def __str__(self):
        print("{0}033[{1};{2}H{3}".format\
        (BLUE_TEXT,self.x,self.y,SYMBOLEJOUEUR))
