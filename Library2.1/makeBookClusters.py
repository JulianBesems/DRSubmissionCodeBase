import time, random, datetime, pygame
from threading import Thread
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingClusters import *
from shelvingUnits import *
from books import Book, BookCollection
from geometries import *
from export import *
from wallPanel import *
from stairs import *

class ClusterCreator:
    def __init__(self, n, envelopes, origin, orientation, size, i, shelfLevels):
        self.n = n
        self.i = i
        self.envelopes = envelopes
        self.clusters = []
        self.size = size
        self.otherClusters = []
        self.origin = origin
        self.orientation = orientation
        #self.floorHeight = floorHeight
        self.shelfLevels = shelfLevels
        self.walkWidth = 1200
        self.wallPanels = None
        self.cs = [[0,'β'], [0,'η'], [0,'σ'], [0,'ρ'], [0,'λ'], [0,'π'], [0,'ψ'], [0,'μ'], [0,'ω'], [0,'α'], [0,'δ']]
        self.maxWallSteps = 10

    def create(self):
        prevCollection = None
        self.cs[0][0] = self.n - 1
        self.cs[1][0] = self.n
        for i in range(self.n):
            books = BookCollection(self.size, i)
            shelves = []
            start = self.origin
            startOrientation = self.orientation
            for b in range(int(self.size/32)):#2**(self.size-5)):
                set = books.books[b*32:b*32+32]
                shelves.append(Shelf(set))
            if i > 0:
                prevCollection = self.clusters[i-1]
                start = prevCollection.shelfColumns[-1].box.pB.translated(0,0, prevCollection.floorHeight + 100)
                startOrientation = prevCollection.shelfColumns[-1].orientation

            #multipleTracks
            otherLeveledClusters = []
            for c in self.otherClusters:
                if len(c.clusters) > i:
                    otherLeveledClusters.append(c.clusters[i])
            shelfCol = ShelvingCollection(shelves, start, startOrientation, self.walkWidth, self.envelopes,
            otherLeveledClusters, self.i, self.shelfLevels, i, self.cs)
            #otherLeveledClusters, self.i, self.shelfLevels - (i/2), i)

            #splitLevels
            #shelfCol = ShelvingCollection(shelves, start, startOrientation, 1000, self.envelope, prevCollection, self.i)

            self.clusters.append(shelfCol)
            made = shelfCol.make()
            if not made:
                print("Fuck this shit, I'm out")
                return False
            walkwayExporter = WalkwayExporter(shelfCol, i)
        self.wallPanels = WallPanels(self, 1200, 75, 10, self.cs)
        self.wallPanels.initiatePanels()
        self.wallPanels.placePanels()
        walls = self.wallPanels.panels
        wallExporter = WallExporter(walls, self.i)
        pillars = Pillars(self.clusters, self.cs)
        pillars.extendPillars()
        stairs = Stairs(self, 250, 1200, 170)
        stairs.makeStairs()
        stairExporter = StairExporter(stairs, self.i)
        exporter = BigExporter(self.clusters, self.i)
        alteredEnvs = []
        for env in range(len(self.envelopes)):
            for e in self.envelopes[env][1:]:
                if not e in alteredEnvs:
                    levelSpan = int(e.h / 3500)
                    grLevel = int(e.pA.z/3500)
                    e.h = 0
                    for i in range(levelSpan):
                        e.h += self.clusters[grLevel + i].floorHeight + 100
                    e.move(0,0,self.clusters[grLevel].origin.z - e.pA.z)
                    alteredEnvs.append(e)
        print(len(alteredEnvs))
        envExporter = EnvelopeExporter(alteredEnvs, self.i)
        print(self.cs)
        return(self.clusters)
