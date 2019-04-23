import pygame, sys, random, time
from geometries import Point, Line, Face, Box
from books import Book, BookCollection
from shelves import Shelf
import numpy as np
import copy

"""pygame.font.init()
myfont = pygame.font.Font('/Users/julianbesems/Library/Fonts/HELR45W.ttf', 28)"""

class Graphics:
    screen_width = 1920 #3360 #1920 #1440 #2560 #1500 #1400 #2000 #1440
    screen_height = 1080 #2100 #1080 #823 #1600 #1000 #800 #1143 #823

    def __init__(self, clusterCreator, envelope):
        self._screen = pygame.display.set_mode((self.screen_width, self.screen_height))#, pygame.FULLSCREEN)
        self.clusters = clusterCreator.clusters
        self.envelope = envelope

    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location

    def draw_screen(self, screen):
        pygame.init()
        pygame.display.set_caption('Recursive bookshelf')

    def draw_line(self, l, color):
        line = self.makeLine(l)
        pygame.draw.line(self._screen, color, line[0], line[1], 2)

    def makeLine(self, l):
        ax = l[0][0]/30 + self.screen_width/5
        ay = l[0][1]/30 + self.screen_height/5
        bx = l[1][0]/30 + self.screen_width/5
        by = l[1][1]/30 + self.screen_height/5
        return [(ax, ay), (bx, by)]

    def makeRect(self, box):
        points = []
        points.append(box.pA)
        points.append(box.pB)
        points.append(box.pC)
        points.append(box.pD)
        points.sort(key = lambda x: x.x + x.y, reverse = True)
        dx = (points[-1].x - points[0].x)/30
        dy = (points[-1].y - points[0].y)/30
        x = points[0].x/30 + self.screen_width/5
        y = points[0].y/30 + self.screen_height/5
        return pygame.Rect(x, y, dx, dy)

    def display(self):

        black = pygame.Color(0,0,0)
        blue = pygame.Color(0,0,200)
        clock = pygame.time.Clock()
        self._screen.fill(pygame.Color('white'))
        self.draw_screen(self._screen)

        iter = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self._screen.fill(pygame.Color('white'))
            black = pygame.Color(0,0,0)
            blue = pygame.Color(000,000,100)

            envelopeLines = []
            for e in self.envelope:
                for l in e.getLines():
                    envelopeLines.append(l)
            for l in envelopeLines:
                self.draw_line(l, black)

            shades = self.getShades()

            for i in range(len(self.clusters)):
                black = pygame.Color(0,0,0)
                blue = pygame.Color(30,30,70)
                c = self.clusters[i]
                blue.r = blue.r + shades[i]
                blue.g = blue.g + shades[i]
                blue.b = blue.b + shades[i]
                black.r = black.r + shades[i]
                black.g = black.g + shades[i]
                black.b = black.b + shades[i]
                for b in c.walkways:
                    pygame.draw.rect(self._screen, blue, self.makeRect(b.box))
                for l in c.drawingGeometry:
                    self.draw_line(l, black)


            pygame.display.update()

            iter +=1

            #time.sleep(0.3)
            clock.tick(400)

    def getShades(self):
        shades = []
        clusters = []
        for c in self.clusters:
            if c.makeing:
                clusters.append(c)
        for i in range(len(clusters)):
            shades.append((len(clusters) - i)*20)
        return shades
