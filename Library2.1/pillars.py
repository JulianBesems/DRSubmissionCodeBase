import pygame, sys, random, time
from geometries import Point, Line, Face, Box
import numpy as np
import copy
import random, string, math

class Pillars:
    def __init__(self, collections, cs):
        self.collections = collections
        self.walkways = []
        self.pillars = self.getPillars()
        self.pillarsExt = self.getPillarsExt()
        self.floorHeights = self.getFloorHeights()
        self.envelopes = self.getEnvelopes()
        self.cs = cs

    def extendPillars(self):
        pillars = []
        for f in range(len(self.floorHeights)-1):
            lengthenPillars = []
            for p in self.pillars[f]:
                p.height += 100
                if not (self.walkwayCollision(self.walkways[f+1], p) or self.envelopeCollision(self.envelopes[f+1], p)):
                    lengthenPillars.append(p)
                else:
                    self.cs[6][0] += 1
            for p in pillars:
                if not (self.walkwayCollision(self.walkways[f+1], p) or self.envelopeCollision(self.envelopes[f+1], p)):
                    lengthenPillars.append(p)
                else:
                    self.cs[6][0] += 1
            pillars = []
            for p in lengthenPillars:
                p.height += (self.floorHeights[f+1] - self.floorHeights[f])
                p.getBox()
                pillars.append(p)

        pillarsExt = []
        for f in range(len(self.floorHeights)-1):
            lengthenPillarsExt = []
            for pe in self.pillarsExt[f]:
                pe.height += 100
                if not (self.walkwayCollision(self.walkways[f+1], pe) or self.envelopeCollision(self.envelopes[f+1], pe)):
                    lengthenPillars.append(pe)
            for pe in pillarsExt:
                if not (self.walkwayCollision(self.walkways[f+1], pe) or self.envelopeCollision(self.envelopes[f+1], pe)):
                    lengthenPillars.append(pe)
            pillarsExt = []
            for pe in lengthenPillarsExt:
                pe.height += (self.floorHeights[f+1] - self.floorHeights[f])
                pe.getBox()
                pillarsExt.append(pe)

    def getPillars(self):
        pillars = []
        self.walkways = []
        for c in self.collections:
            floorPillars = []
            floorWalkways = []
            for w in c.walkways:
                floorWalkways.append(w)
                if not len(w.pillar) == 0:
                    for p in w.pillar:
                        floorPillars.append(p)
            pillars.append(floorPillars)
            self.walkways.append(floorWalkways)
        return pillars

    def getPillarsExt(self):
        pillarsExt = []
        self.walkways = []
        for c in self.collections:
            floorPillars = []
            floorWalkways = []
            for v in c.walkways:
                floorWalkways.append(v)
            for w in c.walkways:
                if not len(w.pillarExt) == 0:
                    for p in w.pillarExt:
                        if self.walkwayCollision(floorWalkways, p):
                            w.pillarExt.remove(p)
                        else:
                            floorPillars.append(p)
            pillarsExt.append(floorPillars)
            self.walkways.append(floorWalkways)
        return pillarsExt

    def getEnvelopes(self):
        envelopes = []
        for e in self.collections[0].envelopes:
            envelopes.append(e[1:])
        return envelopes

    def getFloorHeights(self):
        floorHeights = []
        for p in self.pillars:
            floorHeights.append(p[0].origin.z + p[0].height)
        return floorHeights

    def walkwayCollision(self, walkways, pillar):
        box = pillar.box
        points = [box.pA, box.pB, box.pC, box.pD]
        for p in points:
            for w in walkways:
                wbox = w.box
                xs = sorted([wbox.pA.x, wbox.pC.x])
                ys = sorted([wbox.pA.y, wbox.pC.y])
                if xs[0] < p.x < xs[1] and ys[0] < p.y < ys[1]:
                    return True
        return False

    def envelopeCollision(self, envelopes, pillar):
        box = pillar.box
        points = [box.pA, box.pB, box.pC, box.pD]
        for p in points:
            for e in envelopes:
                xs = sorted([e.pA.x, e.pC.x])
                ys = sorted([e.pA.y, e.pC.y])
                if xs[0] < p.x < xs[1] and ys[0] < p.y < ys[1]:
                    return True
        return False

class Pillar:
    def __init__(self, origin, width, height, orientation):
        self.colour = pygame.Color(200, 200, 200)
        self.origin = origin
        self.width = width
        self.height = height
        self.depth = width
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

    def moveOutAC(self):
        self.getBox()
        dx = self.box.pA.x - self.box.pC.x
        dy = self.box.pA.x - self.box.pC.x
        dz = self.box.pA.x - self.box.pC.x
        self.origin.move(dx, dy, dz)
        self.getBox()

    def moveOutAB(self):
        self.getBox()
        dx = self.box.pA.x - self.box.pB.x
        dy = self.box.pA.x - self.box.pB.x
        dz = self.box.pA.x - self.box.pB.x
        self.origin = self.origin.translated(dx, dy, dz)
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
