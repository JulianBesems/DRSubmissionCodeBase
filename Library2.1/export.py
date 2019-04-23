import time, random, datetime, pygame
from threading import Thread
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingClusters import *
from shelvingUnits import *
from books import Book, BookCollection
from geometries import *

class Exporter:

    def __init__(self, shelvingCollection, i):
        self.shelvingCollection = shelvingCollection
        walkways = []
        books = []
        shelves = []
        walls = []
        pillars = []
        pillarsExt = []
        for w in shelvingCollection.walkways:
            w.box.layer = "Walkways"
            walkways.append(w.box)
            if not len(w.pillar) == 0:
                for p in w.pillar:
                    p.box.layer = "Pillars"
                    pillars.append(p.box)
            if not len(w.pillarExt) == 0:
                for p in w.pillarExt:
                    p.box.layer = "PillarsExt"
                    pillarsExt.append(pe.box)

        for c in shelvingCollection.shelfColumns:
            for s in c.shelves:
                s.box.layer = "Shelves"
                shelves.append(s.box)
                for l in s.walls:
                    l.box.layer = "Walls"
                    walls.append(l.box)
                for b in s.books:
                    b.box.layer = "Books"
                    books.append(b.box)
        self.exportBoxes(walkways, "Walkways", i)
        self.exportBoxes(books, "Books", i)
        self.exportBoxes(shelves, "Shelves", i)
        self.exportBoxes(walls, "Walls", i)
        self.exportBoxes(pillars, "Pillars", i)
        self.exportBoxes(pillars, "PillarsExt", i)
        print("exported" + str(i))


    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + "." + str(self.shelvingCollection.n) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()

class WalkwayExporter:

    def __init__(self, shelvingCollection, i):
        self.shelvingCollection = shelvingCollection
        walkways = []
        for w in shelvingCollection.walkways[1:-1]:
            w.box.layer = "Walkways"
            walkways.append(w.box)
        self.exportBoxes(walkways, "Walkways", i)
        print("exported" + str(i))


    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + "." + str(self.shelvingCollection.n) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()

class StairExporter:
    def __init__(self, stairs, i):
        self.stairs = stairs
        stairs = []
        for s in self.stairs.stairs:
            for t in s:
                t.box.layer = "Stairs"
                stairs.append(t.box)
        self.exportBoxes(stairs, "Stairs", i)

    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()

class EnvelopeExporter:
    def __init__(self, envelopes, i):
        self.envelopes = envelopes
        envs = []
        for e in self.envelopes:
            e.layer = "Envelopes"
            envs.append(e)
        self.exportBoxes(envs, "Envelopes", i)

    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()

class WallExporter:

    def __init__(self, walls, i):
        self.walls = walls
        panels = []
        boards = []
        for w in self.walls:
            w.box.layer = "ExternalWalls"
            panels.append(w.box)
            if not w.floorBoard == None:
                w.floorBoard.box.layer = "FloorBoards"
                boards.append(w.floorBoard.box)
        self.exportBoxes(panels, "ExternalWalls", i)
        self.exportBoxes(boards, "FloorBoards", i)


    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()

class BigExporter:

    def __init__(self, shelvingCollections, i):
        self.shelvingCollections = shelvingCollections
        books = []
        shelves = []
        walls = []
        pillars = []
        pillarsExt = []
        for sc in self.shelvingCollections:
            for w in sc.walkways:
                if not len(w.pillar) == 0:
                    for p in w.pillar:
                        p.box.layer = "Pillars"
                        pillars.append(p.box)
                if not len(w.pillarExt) == 0:
                    for pe in w.pillarExt:
                        pe.box.layer = "PillarsExt"
                        pillarsExt.append(pe.box)
            for c in sc.shelfColumns:
                for s in c.shelves:
                    s.box.layer = "Shelves"
                    shelves.append(s.box)
                    for l in s.walls:
                        l.box.layer = "Walls"
                        walls.append(l.box)
                    for b in s.books:
                        b.box.layer = "Books"
                        books.append(b.box)
        self.exportBoxes(books, "Books", i)
        self.exportBoxes(shelves, "Shelves", i)
        self.exportBoxes(walls, "Walls", i)
        self.exportBoxes(pillars, "Pillars", i)
        self.exportBoxes(pillarsExt, "PillarsExt", i)

    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export3" + str(f) + "_" + str(t) + ".csv", "w+")
        for b in boxes:
                xa = str(b.pA.x)
                ya = str(b.pA.y)
                za = str(b.pA.z)
                xb = str(b.pB.x)
                yb = str(b.pB.y)
                zb = str(b.pB.z)
                xc = str(b.pC.x)
                yc = str(b.pC.y)
                zc = str(b.pC.z)
                h = str(b.h)
                colour = b.colour
                l = b.layer
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)

                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + ", " + l + "\n")
        file.close()
