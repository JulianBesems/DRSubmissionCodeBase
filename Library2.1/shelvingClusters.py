import pygame, sys, random, time
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingUnits import *
from walkways import *
import numpy as np
import copy
import random, string, math
from collections import deque

factor = 1/3

class ShelvingCollection:
    def __init__(self, shelves, origin, orientation, walkWidth, envelopes, otherCollections, n, shelfLevels, level, cs):
        self.shelves = shelves
        self.origin = origin
        self.envelopes = envelopes
        self.level = level
        self.orientation = self.convertOrientation(orientation)
        self.walkWidth = walkWidth
        self.walkways = []
        self.shelfColumns = deque()
        self.shelfColumns.append(ShelvingColumn(1, self.origin, self.orientation, 's', shelfLevels))
        self.otherCollections = otherCollections
        self.drawingGeometry = []
        self.floorHeight = 100
        self.shelfLevels = shelfLevels
        self.makeing = False
        self.n = n
        self.rec = 0
        self.attempts = 0
        self.stairR = None
        self.stairL = None
        self.LeftThresh = 5
        self.rightThresh = 10
        self.averageRel = 0
        self.cs = cs

    def make(self):
        self.makeing = True
        maxDiff = 0
        for s in self.shelves:
            rmax = 11
            #r = random.randint(0,rmax)
            if len(self.shelfColumns) == 1 and len(self.shelfColumns[0].shelves) ==0:
                s.colour = pygame.Color(255,0,0)
                self.shelfColumns[0].placeShelf(s)
            else: # r <= rmax:
                self.placeAbove(s)
            """elif r == rmax-1:
                self.placeLeft(s)
            elif r == rmax:
                self.placeRight(s)"""
        for s in self.shelfColumns:
            s.getBox()
            if self.floorHeight < s.height:
                self.floorHeight = s.height
        for i in range(len(self.shelfColumns)):
            if i > 0:
                relation = abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd)
                self.averageRel += relation
                if abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd) > maxDiff:
                    maxDiff = abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd)
        self.averageRel = self.averageRel/len(self.shelfColumns)
        print(self.averageRel)
        self.LeftThresh = (1 - factor) * self.averageRel
        self.rightThresh = (1+factor) * self.averageRel
        stairR = ShelvingColumn(0, self.origin, self.shelfColumns[-1].orientation, self.shelfColumns[-1].dir, self.shelfLevels)
        stairR.width = 1.47* self.floorHeight + 3000
        stairR.height = self.floorHeight
        stairR.depth = 200
        self.shelfColumns.append(stairR)
        stairL = ShelvingColumn(0, self.origin, self.orientation, self.shelfColumns[-1].dir, self.shelfLevels)
        stairL.width = 1.47 * 2100 + 1200
        stairL.height = self.floorHeight
        stairL.depth = 200
        self.shelfColumns.appendleft(stairL)
        finished = False
        self.stairR = stairR
        self.stairL = stairL
        self.finished = False
        while not self.finished:
            self.getDirections(0)
            self.rec = 0

            if self.attempts > 1:
                for s in self.shelfColumns:
                    s.relInd = random.randint(1,100)
                for i in range(len(self.shelfColumns)):
                    if i > 0:
                        relation = abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd)
                        self.averageRel += relation
                        if abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd) > maxDiff:
                            maxDiff = abs(self.shelfColumns[i].relInd - self.shelfColumns[i-1].relInd)
                self.averageRel = self.averageRel/len(self.shelfColumns)
                print(self.averageRel)
                self.LeftThresh = (1 - factor) * self.averageRel
                self.rightThresh = (1+factor) * self.averageRel

            self.attempts += 1
            if self.attempts == 10:
                return False
        self.shelfColumns[-1].width = self.shelfColumns[-1].width - (stairL.width + 1000)
        self.shelfColumns[-1].getBox()
        for s in self.shelfColumns:
            s.repopulate()
        for w in self.walkways:
            for p in w.pillar:
                p.height = self.floorHeight
        return True

    def getDirections(self, s):
        self.rec +=1
        if self.attempts > 0 and self.rec == 1:
            self.walkways = []
            self.drawingGeometry = []
        if self.rec >= 950:
            return True
        if s == 0:
            self.shelfColumns[0].getBox()
            self.shelfColumns[0].moveTo(self.origin)
            self.shelfColumns[0].changeOrientation(self.orientation)
            self.getCurrentDir(self.shelfColumns[0])
            self.walkways.append(Walkway(self.shelfColumns[0], self.walkWidth, self.floorHeight, None, 0))
            self.drawingGeometry.append(self.shelfColumns[0].box.getLines()[0])
            s = 1
        i = s
        end = False
        while not end:
            self.shelfColumns[i].getBox()
            n = self.getNextDir(i)
            if n == True and i == len(self.shelfColumns)-1:
                end = True
                self.finished = True
                return True
            if n == False:
                self.walkways = self.walkways[:i-1]
                self.drawingGeometry = self.drawingGeometry[:i-1]
                for j in range(i, len(self.shelfColumns)):
                    self.shelfColumns[j].bannedDirs = []
                self.getDirections(i-1)
                end = True
                return True
            i += 1

    def getCurrentDir(self, column):
        s = [1,0,0]
        e = [0,1,0]
        n = [-1,0,0]
        w = [0,-1,0]
        if column.orientation == s:
            column.dir = 's'
        elif column.orientation == e:
            column.dir = 'e'
        elif column.orientation == n:
            column.dir = 'n'
        elif column.orientation == w:
            column.dir = 'w'

    def checkStraight(self, nonIntersectDirs, column):
        for j in range(len(nonIntersectDirs)):
            if nonIntersectDirs[j] == column.dir:
                return j
        return -1

    def getNextDir(self, i):
        columns = self.shelfColumns
        s = [1,0,0]
        e = [0,1,0]
        n = [-1,0,0]
        w = [0,-1,0]
        dirs = ['s', 'e', 'w', 'n']
        orientations = [s, e, w, n]
        nonIntersectDirs = []
        nonIntersectOr = []
        for r in range(0,4):
            overlap = False
            columns[i].dir = dirs[r]
            v = self.getDirVal(columns[i-1].dir, columns[i].dir)
            if not (v == 10 or columns[i].dir in columns[i].bannedDirs or self.check3RTurns(i, v)):
                if v == 0 or v == -1:
                    columns[i].moveTo(columns[i-1].box.pB)
                    columns[i].changeOrientation(orientations[r])
                else:
                    columns[i].moveTo(columns[i-1].box.pC)
                    columns[i].changeOrientation(orientations[r])
                    dx = columns[i].box.pA.x - columns[i].box.pD.x
                    dy = columns[i].box.pA.y - columns[i].box.pD.y
                    dz = columns[i].box.pA.z - columns[i].box.pD.z
                    columns[i].moveTo(columns[i].box.pA.translated(dx, dy, dz))
                columns[i].getBox()
                prevColumns = list(columns)
                prevColumns = prevColumns[0:i-1]
                walkways = self.walkways[0:i-1]
                walkway = Walkway(columns[i], self.walkWidth, self.floorHeight, self.walkways[i-1], v)
                overlap = self.checkOverlap(columns[i], prevColumns, walkways, walkway)
                if not overlap:
                    nonIntersectOr.append(orientations[r])
                    nonIntersectDirs.append(dirs[r])
        if len(nonIntersectOr) == 0:
            columns[i-1].bannedDirs.append(columns[i-1].dir)
            return False
        else:
            #s = self.checkStraight(nonIntersectDirs, columns[i-1])
            if len(nonIntersectOr) == 1:
                r = 0
                columns[i].dir = nonIntersectDirs[r]
                setOrientation = nonIntersectOr[r]
            #elif s >= 0:
            #    r = s
            else:
                tuples = []
                relInd = abs(columns[i-1].relInd - columns[i].relInd)
                for n in range(len(nonIntersectDirs)):
                    tuples.append([nonIntersectDirs[n], nonIntersectOr[n], self.getDirVal(columns[i-1].dir, nonIntersectDirs[n])])
                tuples.sort(key = lambda x : x[2], reverse = True)
                if len(tuples) > 2:
                    if relInd < self.LeftThresh:
                        columns[i].dir = tuples[0][0]
                        setOrientation = tuples[0][1]
                    elif relInd > self.rightThresh:
                        columns[i].dir = tuples[-1][0]
                        setOrientation = tuples[-1][1]
                    else:
                        columns[i].dir = tuples[1][0]
                        setOrientation = tuples[1][1]
                else:
                    if relInd < self.LeftThresh:
                        columns[i].dir = tuples[0][0]
                        setOrientation = tuples[0][1]
                    elif relInd > self.rightThresh:
                        columns[i].dir = tuples[-1][0]
                        setOrientation = tuples[-1][1]
                    elif tuples[0][2] == 0:
                        columns[i].dir = tuples[0][0]
                        setOrientation = tuples[0][1]
                    elif tuples[-1][2] == 0:
                        columns[i].dir = tuples[-1][0]
                        setOrientation = tuples[-1][1]
                    else:
                        if relInd < self.averageRel:
                            columns[i].dir = tuples[1][0]
                            setOrientation = tuples[1][1]
                        else:
                            columns[i].dir = tuples[0][0]
                            setOrientation = tuples[0][1]
            v = self.getDirVal(columns[i-1].dir, columns[i].dir)
            if v == 0:
                columns[i].moveTo(columns[i-1].box.pB)
                columns[i].changeOrientation(setOrientation)
                self.cs[2][0] += 1
            elif v == -1:
                columns[i].moveTo(columns[i-1].box.pB)
                columns[i].changeOrientation(setOrientation)
                self.cs[3][0] += 1
            else:
                columns[i].moveTo(columns[i-1].box.pC)
                columns[i].changeOrientation(setOrientation)
                dx = columns[i].box.pA.x - columns[i].box.pD.x
                dy = columns[i].box.pA.y - columns[i].box.pD.y
                dz = columns[i].box.pA.z - columns[i].box.pD.z
                columns[i].moveTo(columns[i].box.pA.translated(dx, dy, dz))
                if i > 3:
                    vp = self.getDirVal(columns[i-2].dir, columns[i-1].dir)
                    if vp == 1:
                        self.cs[4][0] += -1
                        self.cs[5][0] += 1
                    else:
                        self.cs[4][0] += 1
                else:
                    self.cs[4][0] += 1
            columns[i].getBox()
            col = columns[i]
            walkway = Walkway(col, self.walkWidth, self.floorHeight, self.walkways[i-1], v)
            self.walkways.append(walkway)
            self.drawingGeometry.append(self.shelfColumns[i].box.getLines()[0])
            return True

            #################
            #Temporary export
            """boxes = []
            for c in range(0, i):
                columns[c].getBox()
                boxes.append(self.walkways[c].box)
                boxes.append(columns[c].box)
            self.exportBoxes(boxes, 3, i)"""
            #################

    def check3RTurns(self, i, v):
        v1 = self.getDirVal(self.shelfColumns[i-2].dir, self.shelfColumns[i-1].dir)
        v2 = self.getDirVal(self.shelfColumns[i-3].dir, self.shelfColumns[i-2].dir)
        if v + v1 + v2 == 3:
            return True
        return False

    def checkOverlap(self, newColumn, prevColumns, walkways, walkway):
        linesA1 = newColumn.box.getLines()
        linesA2 = copy.deepcopy(linesA1)
        if not walkway == None:
            linesW1 = walkway.box.getLines()
            for l in linesW1:
                linesA1.append(l)
        linesE = []
        for e in self.envelopes[self.level]:
            for l in e.getLines():
                linesE.append(l)

        for lx in linesA1:
            for ly in linesE:
                if self.intersects(lx, ly):
                    return True

        #for split levels
        """if not self.otherCollections == None:
            for pc in self.otherCollections.shelfColumns:
                if pc.height > self.floorHeight:
                    pc.getBox()
                    linesW = pc.box.getLines()
                    for lx in linesA1:
                        for ly in linesW:
                            if self.intersects(lx, ly):
                                return True"""

        #for multiple tracks
        if not self.otherCollections == []:
            for oc in self.otherCollections:
                for pw in oc.walkways:
                    linesW = pw.box.getLines()
                    for lx in linesA1:
                        for ly in linesW:
                            if self.intersects(lx, ly):
                                return True

        for x in prevColumns:
            linesB = x.box.getLines()
            for lx in linesA1:
                for ly in linesB:
                    if self.intersects(lx, ly):
                        return True
        for w in walkways:
            linesC = w.box.getLines()
            for lx in linesA2:
                for ly in linesC:
                    if self.intersects(lx, ly):
                        return True

        if (not (self.level == len(self.envelopes) -1)
        and len(self.walkways) >= (len(self.shelfColumns) - 2)):
            linesW = walkway.box.getLines()
            linesEN = []
            for e in self.envelopes[self.level + 1]:
                for l in e.getLines():
                    linesEN.append(l)
            #print(len(linesEN))
            for lx in linesW:
                for ly in linesEN:
                    if self.intersects(lx, ly):
                        return True
        return False

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    def intersects(self, l1, l2):
        L1 = self.line(l1[0], l1[1])
        L2 = self.line(l2[0], l2[1])
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            x1 = min(l1[0][0], l1[1][0])
            x2 = max(l1[0][0], l1[1][0])
            y1 = min(l1[0][1], l1[1][1])
            y2 = max(l1[0][1], l1[1][1])
            x3 = min(l2[0][0], l2[1][0])
            x4 = max(l2[0][0], l2[1][0])
            y3 = min(l2[0][1], l2[1][1])
            y4 = max(l2[0][1], l2[1][1])
            if (((x1 < x < x2) and (y3 < y < y4)) or
                ((x3 < x < x4) and (y1 < y < y2))):
                return True
        else:
            return False


    def getDirVal(self, p, c):
        if p == 's':
            if c == 's':
                return 0
            if c == 'e':
                return 1
            if c == 'w':
                return -1
            if c == 'n':
                return 10
        elif p == 'e':
            if c == 'e':
                return 0
            if c == 'n':
                return 1
            if c == 's':
                return -1
            if c == 'w':
                return 10
        elif p == 'n':
            if c == 'n':
                return 0
            if c == 'w':
                return 1
            if c == 'e':
                return -1
            if c == 's':
                return 10
        elif p == 'w':
            if c == 'w':
                return 0
            if c == 's':
                return 1
            if c == 'n':
                return -1
            if c == 'e':
                return 10

    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def placeAbove(self, shelf):
        columns = []
        for c in self.shelfColumns:
            if not c.isFull():
                columns.append(c)
        if len(columns) == 0:
            relInd1 = abs(self.shelfColumns[0].relInd - shelf.relInd)
            relInd2 = abs(self.shelfColumns[-1].relInd - shelf.relInd)
            if relInd1 < relInd2:
                self.placeLeft(shelf)
            else:
                self.placeRight(shelf)
        else:
            min = abs(columns[0].relInd - shelf.relInd)
            index = 0
            for c in range(len(columns)):
                if abs(columns[c].relInd - shelf.relInd) < min:
                    min = abs(columns[0].relInd - shelf.relInd)
                    index = c
            columns[index].placeShelf(shelf)

    def placeLeft(self, shelf):
        l = self.shelfColumns[0]
        ll = ShelvingColumn(l.hierarchy + 1, self.origin, l.orientation, l.dir, self.shelfLevels)
        ll.placeShelf(shelf)
        self.shelfColumns.appendleft(ll)

    def placeRight(self, shelf):
        r = self.shelfColumns[-1]
        rr = ShelvingColumn(r.hierarchy + 1, self.origin, r.orientation, r.dir, self.shelfLevels)
        rr.placeShelf(shelf)
        self.shelfColumns.append(rr)

    def exportBoxes(self, boxes, f, t):
        file = open("Exports/export" + str(f) + "_" + str(t) + ".csv", "w+")
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
                r = str(colour.r)
                g = str(colour.g)
                b = str(colour.b)
                a = str(colour.a)
                file.write(xa + ", " + ya + ", " + za + ", " + xb + ", " + yb + ", " + zb + ", " +xc + ", " + yc + ", " + zc + ", " + h + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
        file.close()
