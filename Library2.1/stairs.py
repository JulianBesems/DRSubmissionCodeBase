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
from floorBoard import *

class Stairs:
    def __init__(self, clusterCreator, width, depth, height):
        self.clusterCreator = clusterCreator
        self.width = width
        self.depth = depth
        self.height = height
        self.clusters = self.clusterCreator.clusters
        self.floors = self.clusterCreator.n
        self.stairs = []

    def makeStairs(self):
        for n in range(self.floors):
            cluster = self.clusters[n]
            staircase = []
            floorheight = cluster.floorHeight
            col = cluster.shelfColumns[-1]
            col.width = self.width
            col.getBox()
            walkway = Step(col.box.colour, col.box.pB.translated(0,0,-100),
                    self.depth, 100, self.depth, col.orientation)
            staircase.append(walkway)
            while ((len(staircase)-1) * self.height < floorheight - self.height):
                staircase.append(Step(col.box.colour, staircase[-1].box.pB.translated(0,0,staircase[-1].height),
                        self.width, self.height, self.depth, col.orientation))
            staircase.append(Step(col.box.colour, staircase[-1].box.pB.translated(0,0,staircase[-1].height),
                    self.depth, self.height, self.depth, col.orientation))
            cluster.walkways = cluster.walkways[1:-1]
            self.stairs.append(staircase)

class Step:
    def __init__(self, colour, origin, width, height, depth, orientation):
        self.colour = colour
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
