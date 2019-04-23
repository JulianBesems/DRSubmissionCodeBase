import time, random, datetime, pygame
from threading import Thread
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingClusters import *
from shelvingUnits import *
from books import Book, BookCollection
from geometries import *
from makeBookClusters import *
from export import Exporter, BigExporter, EnvelopeExporter
from showAlgorithm import Graphics
import sys
import csv

class Main:
    def __init__(self, argumentList):
        self.time = datetime.datetime.now()
        self.stories = int(argumentList[1])
        self.envelopes = self.getEnvelopes()


    def getEnvelopes(self):
        envelopes =[]
        with open('externalEnvelope.txt', mode = 'r', encoding = 'utf-8-sig') as csv_ext:
            csvReaderExt = csv.reader(csv_ext, delimiter = ',')
            extPs = []
            for row in csvReaderExt:
                extPs.append(Point(int(round(float(row[0]))), int(round(float(row[1][1:]))), int(round(float(row[2][1:])))))
            externalEnvelope = Box(pygame.Color(0,100,0), extPs[0], extPs[3],
                                    extPs[2], extPs[1], extPs[4].z - extPs[0].z)
        for i in range(self.stories):
            envelopes.append([externalEnvelope])

        with open('internalEnvelopes.txt', mode = 'r', encoding = 'utf-8-sig') as csv_int:
            csvReaderInt = csv.reader(csv_int, delimiter = ',')
            intPoints = []
            for row in csvReaderInt:
                intPoints.append(Point(int(round(float(row[0]))), int(round(float(row[1][1:]))), int(round(float(row[2][1:])))))
            for i in range(int(len(intPoints)/ 8)):
                envPs = []
                for j in range(8):
                    envPs.append(intPoints[i* 8 + j])
                env = Box(pygame.Color(0,100,0), envPs[0], envPs[3],
                                    envPs[2], envPs[1], envPs[4].z - envPs[0].z)
                levelSpan = int(env.h / 3500)
                grLevel = int(env.pA.z/3500)
                for x in range(levelSpan):
                    envelopes[x + grLevel].append(env)
        return envelopes

    def run(self):

        envelopes = self.envelopes
        origin1 = Point(10000, 12000, 0)
        #origin2 = Point(28000, 11000, 0)
        #origin3 = Point((3/4)*self.envelopeWidth, self.envelopeDepth - 100, 0)
        """origin4 = Point((3/4)*self.envelopeWidth, self.envelopeDepth - 100, 0)
        origin7 = Point((3/4)*self.envelopeWidth, 100, 0)
        origin8 = Point((1/4)*self.envelopeWidth, 100, 0)
        origin5 = Point(self.envelopeWidth - 100, (3/4)*self.envelopeDepth, 0)
        origin6 = Point(self.envelopeWidth - 100, (1/4)*self.envelopeDepth, 0)"""
        orientation1 = [1,0,0]
        #orientation2 = [-1,0,0]
        #orientation3 = [0,-1,0]
        """orientation4 = [0,-1,0]
        orientation7 = [0,1,0]
        orientation8 = [0,1,0]
        orientation5 = [-1,0,0]
        orientation6 = [-1,0,0]"""
        size = int(2**17/self.stories)
        clusterCreator1 = ClusterCreator(self.stories, envelopes, origin1, orientation1, size, 0, 8)
        #clusterCreator2 = ClusterCreator(2, [envelope1, envelope2, lectureTheatre], origin2, orientation2, size, 1, 10)
        #clusterCreator3 = ClusterCreator(self.n, envelope, origin3, orientation3, size, 2)
        """clusterCreator4 = ClusterCreator(self.n, envelope, origin4, orientation4, size, 3)
        clusterCreator5 = ClusterCreator(self.n, envelope, origin5, orientation5, size, 4)
        clusterCreator6 = ClusterCreator(self.n, envelope, origin6, orientation6, size, 5)
        clusterCreator7 = ClusterCreator(self.n, envelope, origin7, orientation7, size, 6)
        clusterCreator8 = ClusterCreator(self.n, envelope, origin8, orientation8, size, 7)"""

        #clusterCreator2.otherClusters = [clusterCreator1]
        clusterCreator1.otherClusters = []
        #clusterCreator3.otherClusters = [clusterCreator2, clusterCreator1]

        """clusterCreator1.otherClusters = [clusterCreator2, clusterCreator3,
                                        clusterCreator4, clusterCreator5, clusterCreator6,
                                        clusterCreator7, clusterCreator8]
        clusterCreator2.otherClusters = [clusterCreator1, clusterCreator3,
                                        clusterCreator4, clusterCreator5, clusterCreator6,
                                        clusterCreator7, clusterCreator8]
        clusterCreator3.otherClusters = [clusterCreator1, clusterCreator2,
                                        clusterCreator4, clusterCreator5, clusterCreator6,
                                        clusterCreator7, clusterCreator8]
        clusterCreator4.otherClusters = [clusterCreator1, clusterCreator2, clusterCreator3,
                                        clusterCreator5, clusterCreator6,
                                        clusterCreator7, clusterCreator8]
        clusterCreator5.otherClusters = [clusterCreator1, clusterCreator2, clusterCreator3,
                                        clusterCreator4, clusterCreator6,
                                        clusterCreator7, clusterCreator8]
        clusterCreator6.otherClusters = [clusterCreator1, clusterCreator2, clusterCreator3,
                                        clusterCreator4, clusterCreator5,
                                        clusterCreator7, clusterCreator8]
        clusterCreator7.otherClusters = [clusterCreator1, clusterCreator2, clusterCreator3,
                                        clusterCreator4, clusterCreator5, clusterCreator6,
                                        clusterCreator8]
        clusterCreator8.otherClusters = [clusterCreator1, clusterCreator2, clusterCreator3,
                                        clusterCreator4, clusterCreator5, clusterCreator6,
                                        clusterCreator7]

        clusters = [clusterCreator1, clusterCreator2, clusterCreator3, clusterCreator4,
                    clusterCreator5, clusterCreator6, clusterCreator7, clusterCreator8]

        finished = False
        i = 0
        while not finished:
            if clusters[i].create():
                i+=1
                if i == len(clusters):
                    finished = True
            else:
                i -=1
                clusters[i].create()"""

        #thread1 = Thread(target = clusterCreator1.create, name = str(1), daemon = True)
        #thread2 = Thread(target = clusterCreator2.create, name = str(1), daemon = True)
        #thread3 = Thread(target = clusterCreator3.create, name = str(1), daemon = True)
        #thread1.start()
        #thread2.start()
        #thread3.start()

        clusterCreator1.create()
        #clusterCreator2.create()

        #exporter = BigExporter(clusterCreator1.clusters, 1)
        #exporter = BigExporter(clusterCreator2.clusters, 2)

        #graphics = Graphics(clusterCreator1, envelopes[0])
        #graphics.display()



        #while True:
        #    pass

argumentList = sys.argv
main = Main(argumentList)
main.run()
