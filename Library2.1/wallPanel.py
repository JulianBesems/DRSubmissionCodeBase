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

class WallPanels:
    def __init__(self, clusterCreator, width, depth, maxSteps, cs):
        self.clusterCreator = clusterCreator
        self.width = width
        self.depth = depth
        self.clusters = self.clusterCreator.clusters
        self.floors = self.clusterCreator.n
        self.panels = []
        self.maxSteps = maxSteps
        self.oneFloorNr = 0
        self.cs = cs

    def initiatePanels(self):
        for n in range(self.floors):
            envelope = self.clusterCreator.envelopes[n][0]
            height = self.clusters[n].floorHeight + 100
            z = self.clusters[n].origin.z - 100
            lines = envelope.getLines()
            oneFloorNr = 0
            for x in lines:
                l = Line(None, Point(x[0][0], x[0][1], 0), Point(x[1][0], x[1][1], 0))
                row = []
                oX = l.pointB.x - l.pointA.x
                oY = l.pointB.y - l.pointA.y
                oZ = l.pointB.z - l.pointA.z
                outward = self.convertOrientation([oY, -oX, oZ])
                inward = self.convertOrientation([oY, oX, oZ])
                length = math.sqrt(oX**2 + oY**2 + oZ**2)
                nr = int(length/self.width)
                oneFloorNr += nr
                origin = l.pointA.translated(outward[0]*self.depth,
                                            outward[1]*self.depth,
                                            z)
                self.panels.append(WallPanel(pygame.Color(150, 100, 100), origin,
                                            self.width, self.depth, height, [oX, oY, oZ], outward, inward, n))
                for i in range(1, nr):
                    self.panels.append(WallPanel(pygame.Color(150, 100, 100),
                                        self.panels[-1].getBox(self.panels[-1].depth).pB, self.width,
                                        self.depth, height, [oX, oY, oZ], outward, inward, n))
                    #print(str(self.panels[-1].origin.x) + ", " + str(self.panels[-1].origin.y))
            self.oneFloorNr = oneFloorNr
        self.cs[7][0] = len(self.panels)


    def convertOrientation(self, d):
        l = math.sqrt(d[0]**2 + d[1]**2)
        return [d[0]/l, d[1]/l, 0]

    def placePanels(self):
        lines = []
        for c in range(len(self.clusters)):
            floorLines = []
            envelopes = self.clusterCreator.envelopes[c][1:]
            for e in envelopes:
                for l in e.getLines():
                    floorLines.append(l)
            for w in self.clusters[c].walkways:
                box = w.box
                for l in box.getLines():
                    floorLines.append(l)
            lines.append(floorLines)

        for p in range(len(self.panels)):
            pan = self.panels[p]
            pLines = pan.intersectBox.getLines()
            eLines = lines[pan.floor]
            iter = 0
            overlap = self.checkOverlap(pLines, eLines)
            while (not overlap) and iter < self.maxSteps:
                if p >= self.oneFloorNr and pan.floorBoard == None:
                    opp = self.panels[p-self.oneFloorNr].origin
                    op = pan.origin
                    if opp.x == op.x and opp.y == op.y:
                        pan.floorBoard = FloorBoard(pan.colour, pan.origin.translated(0,0,0),
                         pan.width, 100, pan.width, pan.orientation, pan.floor)
                elif not pan.floorBoard == None:
                    pan.floorBoard.depth += pan.width
                    pan.floorBoard.box = pan.floorBoard.getBox()
                pan.moveTo(pan.outerBox.pD.translated(0,0,0))
                pLines = pan.intersectBox.getLines()
                overlap = self.checkOverlap(pLines, eLines)
                iter +=1
            #Indent remove
            #if iter == self.maxSteps:
            #    pan.floorBoard = None
            if iter > 0:
                self.cs[9][0] += 1
                self.cs[10][0] += 1
            if iter > 1:
                self.cs[8][0] += iter - 2


    def checkOverlap(self, lines1, lines2):
        for lx in lines1:
            for ly in lines2:
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


class WallPanel:
    def __init__(self, colour, origin, width, depth, height, orientation, outward, inward, floor):
        self.colour = colour
        self.origin = origin
        self.width = width
        self.height = height
        self.depth = depth
        self.orientation = self.convertOrientation(orientation)
        self.box = self.getBox(self.depth)
        self.outerBox = self.getBox(self.width)
        self.intersectBox = self.getBox(self.width + self.depth)
        self.outward = outward
        self.inward = inward
        self.floor = floor
        self.floorBoard = None

    def getBox(self, depth):
        a = self.origin
        b = a.translated(self.width * self.orientation[0],
                        self.width * self.orientation[1],
                        self.width * self.orientation[2])
        d = a.translated(depth * -self.orientation[1],
                        depth * self.orientation[0],
                        depth * self.orientation[2])
        c = b.translated(depth * -self.orientation[1],
                        depth * self.orientation[0],
                        depth * self.orientation[2])

        box = Box(self.colour, a, b, c, d, self.height)
        return box

    def move(self, x, y, z):
        self.origin.move(x, y, z)
        self.box = self.getBox(self.depth)
        self.outerBox = self.getBox(self.width)
        self.intersectBox = self.getBox(self.width + self.depth)

    def moveTo(self, p):
        self.origin = p
        self.box = self.getBox(self.depth)
        self.outerBox = self.getBox(self.width)
        self.intersectBox = self.getBox(self.width + self.depth)

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
        self.outerBox = self.getBox(self.width)
        self.intersectBox = self.getBox(self.width + self.depth)
