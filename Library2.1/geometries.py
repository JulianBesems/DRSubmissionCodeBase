import pygame, sys, random, time
import numpy as np
import math, copy

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

class Line:
    def __init__(self, colour, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.colour = colour

    def move(self, x, y, z):
        self.pointA.move(x, y, z)
        self.pointB.move(x, y, z)

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

class Face:
    def __init__(self, colour, pA, pB, pC, pD):
        self.pA = pA
        self.pB = pB
        self.pC = pC
        self.pD = pD
        self.colour = colour
        self.colourC = self.colour

    def move(self, x, y, z):
        self.pA.move(x, y, z)
        self.pB.move(x, y, z)
        self.pC.move(x, y, z)
        self.pD.move(x, y, z)

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

class Box:
    def __init__(self, colour, pA, pB, pC, pD, h):
        self.h = h
        self.pA = pA
        self.pB = pB
        self.pC = pC
        self.pD = pD
        self.colour = colour
        self.layer = None

    def move(self, x, y, z):
        self.pA.move(x, y, z)
        self.pB.move(x, y, z)
        self.pC.move(x, y, z)
        self.pD.move(x, y, z)

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

    def getLines(self):
        l1 = [(self.pA.x, self.pA.y),
                (self.pB.x, self.pB.y)]
        l2 = [(self.pC.x, self.pC.y),
                (self.pD.x, self.pD.y)]
        l3 = [(self.pD.x, self.pD.y),
                (self.pA.x, self.pA.y)]
        l4 = [(self.pB.x, self.pB.y),
                (self.pC.x, self.pC.y)]
        return[l1, l2, l3, l4]
