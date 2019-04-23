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

class Walkway:
    def __init__(self, col, walkWidth, height, pWalkway, v):
        self.walkWidth = walkWidth
        self.pWalkway = pWalkway
        self.height = height
        self.col = col
        self.orientation = col.orientation
        self.v = v
        self.pA = col.box.pA.translated(0,0,-100)
        self.pB = col.box.pB.translated(0,0,-100)
        self.pC = col.box.pC.translated(self.walkWidth * -col.orientation[1],
                            self.walkWidth * col.orientation[0],
                            self.walkWidth * col.orientation[2] - 100)
        self.pD = col.box.pD.translated(self.walkWidth * -col.orientation[1],
                            self.walkWidth * col.orientation[0],
                            self.walkWidth * col.orientation[2] - 100)
        self.box = Box(pygame.Color(0, 0, 255), self.pA, self.pB, self.pC, self.pD, 100)
        self.pillar = []
        self.pillarExt = []
        self.finaliseWalkway()

    def getBox(self):
        self.box = Box(pygame.Color(0, 0, 255), self.pA, self.pB, self.pC, self.pD, 100)

    def finaliseWalkway(self):
        if self.v == -1:
            dx = self.pWalkway.pC.x - self.pA.x
            dy = self.pWalkway.pC.y - self.pA.y
            dz = self.pWalkway.pC.z - self.pA.z
            self.pA = self.pA.translated(dx, dy, dz)
            self.pD = self.pD.translated(dx, dy, dz)
            self.getBox()
            p = Pillar(self.pWalkway.box.pB.translated(0,0,0), 100, self.height, self.pWalkway.orientation)
            self.pillar.append(p)
            pe = Pillar(self.box.pD.translated(0,0,0), 100, self.height, self.pWalkway.orientation)
            self.pillarExt.append(pe)

        if self.v == 1:
            p = Pillar(self.col.box.pD.translated(0,0,-100), 100, self.height, self.orientation)
            dx = p.box.pA.x - p.box.pC.x
            dy = p.box.pA.y - p.box.pC.y
            dz = p.box.pA.z - p.box.pC.z
            p.moveTo(p.box.pA.translated(dx, dy, dz))
            self.pillar.append(p)
