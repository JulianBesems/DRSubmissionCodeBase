import time, random, datetime, pygame
from threading import Thread
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingClusters import *
from shelvingUnits import *
from books import Book, BookCollection
from geometries import *

levels = 6

def writeFile(nr, min, max):
    minWidth = 5
    maxWidth = 50
    minDepth = 100
    maxDepth = 200
    minRatDH = 8
    maxRatDH = 20
    for i in range(levels):
        file = open("bookIndexesA" + str(i) + ".csv", "w+")
        for b in range(0,nr):
            width = str(random.randint(minWidth, maxWidth))
            depth = str(random.randint(minDepth, maxDepth))
            height = str(int(random.randint(minRatDH, maxRatDH)/10 * int(depth)))
            relInd = str(random.randint(min, max))
            name = random.choice(string.ascii_letters)
            file.write(str(random.randint(min, max)) +", " + random.choice(string.ascii_letters) + ", " + width + ", " + depth + ", " + height + "\n")
        file.close()

writeFile((int((2**17)/levels)), 0, 100)
