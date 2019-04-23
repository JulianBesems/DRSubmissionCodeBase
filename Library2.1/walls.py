import pygame, sys, random, time
from geometries import Point, Line, Face, Box
import numpy as np
import copy
import random, string, math

class Wall:
    def __init__(self, origin, width, depth, height, orientation):
        self.colour = pygame.Color(200, 200, 200)
        self.origin = origin
        self.width = width
        self.height = height
        self.depth = depth
        self.orientation = self.convertOrientation(orientation)
        self.box = self.getBox()

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

        self.box = Box(self.colour, a, b, c, d, self.height)
        return self.box

    def moveOutAB(self):
        self.getBox()
        dx = self.box.pA.x - self.box.pB.x
        dy = self.box.pA.y - self.box.pB.y
        dz = self.box.pA.z - self.box.pB.z
        self.moveTo(self.box.pA.translated(dx, dy, dz))
        self.box = self.getBox()

    def move(self, x, y, z):
        self.origin.move(x, y, z)
        self.box = self.getBox()

    def moveTo(self, p):
        self.origin = p
        self.box = self.getBox()

    def changeOrientation(self, o):
        self.orientation = self.convertOrientation(o)
        self.box = self.getBox()

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]
