import pygame, sys, random, time
from geometries import Point, Line, Face, Box
import numpy as np
import copy
import random, string, math
import sys
import csv

class Book:
    def __init__(self, name, colour, origin, width, depth, height, orientation):
        if name == None:
            self.name = random.choice(string.ascii_letters)
        else:
            self.name = name
        self.colour = colour
        self.relInd = 0
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
        self.box = self.getBox()

    def moveTo(self, p):
        self.origin = p
        self.box = self.getBox()

    def translated(self, x, y, z):
        a = copy.deepcopy(self)
        a.move(x, y, z)
        return a

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def changeOrientation(self, o):
        self.orientation = self.convertOrientation(o)
        self.box = self.getBox()

class BookCollection:
    def __init__(self, n, floor):
        self.floor = floor
        self.books = self.getBooks(n)

    def getBooks(self, n):
        minWidth = 5
        maxWidth = 50
        minDepth = 100
        maxDepth = 200
        minRatDH = 8
        maxRatDH = 20
        books = []
        with open("bookIndexesT" + str(self.floor) + ".csv") as csv_ext:
            csvReaderExt = csv.reader(csv_ext, delimiter = ',')
            extPs = []
            for row in csvReaderExt:
                c = pygame.Color(random.randint(0,255), random.randint(0,255),
                                random.randint(0,255))
                o = Point(0, 0, 0)
                width = int(row[2])
                depth = int(row[3])
                height = int(row[4])
                book = Book(None, c, o, width, depth, height, [1,0,0])
                book.relInd = int(row[0])
                book.name = str(row[1])
                books.append(book)
        averageRel = 0
        for b in books:
            averageRel += b.relInd
        averageRel = averageRel/len(books)
        s = sorted(books, key=lambda x: x.width * x.depth * x.height, reverse=True)
        #s = sorted(books, key=lambda x: x.name, reverse=True)
        #s = sorted(books, key=lambda x: abs(x.relInd - averageRel))
        print(len(books))
        return s
