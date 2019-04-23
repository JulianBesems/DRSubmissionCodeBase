import pygame, sys, random, time
from geometries import Point, Line, Face, Box
import numpy as np
import copy
import random, string, math
from walls import Wall
from collections import deque

class Shelf:
    def __init__(self, books):
        self.colour = pygame.Color(200, 200, 200)
        self.relInd = 0
        self.width = 0
        self.highestBook = 0
        self.height = 20
        self.depth = 200
        self.orientation = books[0].orientation
        self.walls = []
        bookDeq = deque()
        bookDeq.append(books[0])
        for i in range(1, len(books)):
            b = books[i]
            b.orientation = self.orientation
            if b.relInd < books[i-1].relInd:
                r = 0
            else:
                r = 1
            if r == 0:
                bookDeq.appendleft(b)
            else:
                bookDeq.append(b)
            self.width += b.width
            if b.height > self.highestBook:
                self.highestBook = b.height
        bookDeq[0].moveTo(Point(0,0,0))
        for i in range(1, len(bookDeq)):
            bookDeq[i].moveTo(copy.deepcopy(bookDeq[i-1].box.pB))
        self.books = bookDeq
        relIndexes = 0
        for b in self.books:
            relIndexes += b.relInd
        self.relInd = relIndexes/len(self.books)
        self.origin = bookDeq[0].origin.translated(0,0,-self.height)
        self.box = self.getBox()
        wallWidth = 20
        self.walls.append(Wall(self.box.pA.translated(0,0,self.height), wallWidth,
                        self.depth, self.highestBook, self.orientation))
        self.walls.append(Wall(self.box.pB.translated(0,0,self.height), wallWidth,
                        self.depth, self.highestBook, self.orientation))
        self.walls[0].moveOutAB()
        self.origin = self.walls[0].origin.translated(0,0,-self.height)
        self.width += wallWidth * 2
        self.getBox()

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def placeBooks(self):
        self.books[0].moveTo(self.origin)
        for i in range(1, len(self.books)):
            self.books[i].moveTo(copy.deepcopy(self.books[i-1].box.pB))


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
        for w in self.walls:
            w.move(x,y,z)
        for b in self.books:
            b.move(x, y, z)
        self.box = self.getBox()


    def moveTo(self, p):
        self.origin = p
        self.box = self.getBox()
        self.walls[0].moveTo(self.box.pA.translated(0,0,self.height))
        self.walls[1].moveTo(self.box.pB.translated(0,0,self.height))
        self.walls[1].moveOutAB()
        self.books[0].moveTo(self.walls[0].box.pB.translated(0,0,0))
        for i in range(1, len(self.books)):
            self.books[i].moveTo(self.books[i-1].box.pB)

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

    def changeOrientation(self, o):
        self.orientation = self.convertOrientation(o)
        self.box = self.getBox()
        for w in self.walls:
            w.changeOrientation(self.orientation)
        self.walls[0].moveTo(self.box.pA.translated(0,0,self.height))
        self.walls[1].moveTo(self.box.pB.translated(0,0,self.height))
        self.walls[1].moveOutAB()
        for b in self.books:
            b.changeOrientation(self.orientation)
        self.books[0].moveTo(self.walls[0].box.pB.translated(0,0,0))
        for i in range(1, len(self.books)):
            self.books[i].moveTo(self.books[i-1].box.pB)
        self.box = self.getBox()
