import pygame, sys, random, time
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingUnits import *
from pillars import *
import numpy as np
import copy
import random, string, math
from collections import deque
from shapely.geometry import LineString

class FloorBoard:
    def __init__(self, colour, origin, width, height, depth, orientation, floor):
        self.colour = colour
        self.origin = origin
        self.width = width
        self.height = height
        self.depth = depth
        self.orientation = self.convertOrientation(orientation)
        self.box = self.getBox()
        self.floor = floor

    def getBox(self):
        a = self.origin
        b = a.translated(self.width * self.orientation[0],
                        self.width * self.orientation[1],
                        self.width * self.orientation[2])
        d = a.translated(self.depth * -self.orientation[1],
                        self.depth * self.orientation[0],
                        self.depth * self.orientation[2])
        c = b.translated(self.depth * -self.orientation[1],
                        self.depth * self.orientation[0],
                        self.depth * self.orientation[2])

        box = Box(self.colour, a, b, c, d, self.height)
        return box

    def move(self, x, y, z):
        self.origin.move(x, y, z)
        self.box = self.getBox(self.depth)

    def moveTo(self, p):
        self.origin = p
        self.box = self.getBox(self.depth)

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def changeOrientation(self, o):
        self.orientation = self.convertOrientation(o)
        self.box = self.getBox(self.depth)
