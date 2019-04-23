import pygame, sys, random, time
from geometries import Point, Line, Face, Box
import numpy as np
import copy
import random, string, math
from collections import deque

class ShelvingColumn:
    def __init__(self, hierarchy, origin, orientation, dir, shelfLevels):
        self.origin = origin
        self.dir = dir
        self.width = 0
        self.height = 0
        self.depth = 0
        self.relInd = 0
        self.box = None
        self.orientation = self.convertOrientation(orientation)
        self.shelves = []
        self.hierarchy = hierarchy
        self.colour = pygame.Color(200, 200, 200)
        self.walls = None
        self.maxLevels = shelfLevels
        self.bannedDirs = []

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def getBox(self):
        if self.height == 0 and self.depth == 0 and self.width ==0:
            for s in self.shelves:
                self.height += s.highestBook + s.height
                if s.depth > self.depth:
                    self.depth = s.depth
                if s.width > self.width:
                    self.width = s.width

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

    def placeShelf(self, s):
        if len(self.shelves) == 0:
            s.moveTo(self.origin)
            s.changeOrientation(self.orientation)
            s.getBox()
            self.shelves.append(s)
        else:
            sp = self.shelves[-1]
            s.moveTo(sp.origin.translated(0,0,sp.highestBook + sp.height))
            s.changeOrientation(self.orientation)
            s.getBox()
            self.shelves.append(s)
        relIndexes = 0
        for s in self.shelves:
            relIndexes += s.relInd
        self.relInd = relIndexes/len(self.shelves)

    def isFull(self):
        if(len(self.shelves) < self.maxLevels):
            return False
        else:
            return True

    def move(self, x, y, z):
        self.origin.move(x, y, z)
        """if not len(self.shelves) == 0:
            for b in self.shelves:
                b.move(x, y, z)"""
        self.getBox()

    def moveTo(self, p):
        self.origin = p
        """if not len(self.shelves) == 0:
            self.shelves[0].moveTo(self.origin)
            for i in range(1, len(self.shelves)):
                s = self.shelves[i]
                sp = self.shelves[i-1]
                s.moveTo(sp.origin.translated(0, 0, sp.highestBook + sp.height))"""
        self.getBox()

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

    def changeOrientation(self, o):
        self.orientation = self.convertOrientation(o)
        """if not len(self.shelves) == 0:
            for s in self.shelves:
                s.changeOrientation(o)"""
        self.box = self.getBox()

    def repopulate(self):
        if not len(self.shelves) == 0:
            self.shelves[0].moveTo(self.origin)
            self.shelves[0].changeOrientation(self.orientation)
            for i in range(1, len(self.shelves)):
                s = self.shelves[i]
                s.changeOrientation(self.orientation)
                sp = self.shelves[i-1]
                s.moveTo(sp.origin.translated(0, 0, sp.highestBook + sp.height))
