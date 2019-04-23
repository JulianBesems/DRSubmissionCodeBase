import time, random, pygame
from threading import Thread

colours = []
colours.append([228, 197, 73])
colours.append([185, 0, 37])
colours.append([78, 87, 111])
colours.append([12, 63, 50])
colours.append([236, 110, 0])
colours.append([68, 22, 33])
colours.append([143, 149, 160])
colours.append([185, 197, 201])
colours.append([35, 127, 125])
colours.append([149, 132, 103])
colours.append([0, 44, 125])
colours.append([0, 160, 213])
colours.append([166, 202, 87])
colours.append([228, 166, 156])

class ConPix:
    def __init__(self):
        self.group = None
        self.pr_group = None
        self.height = 0
        self.colour = pygame.Color(255, 255, 255)
        self.new = False
        self.removed = False
        self.dates = []
        self.contents = []

    def checkDates(self, date, threshold):
        dateHeight = 0
        for d in self.dates:
            if d <= (int(date - threshold)):
                dateHeight += 1
        if self.height < dateHeight:
            dateHeight = self.height
        return dateHeight

    def add(self, group, date, content):
        self.group = group
        if self.height < 5:
            self.height += 1
        if len(self.dates) < 5:
            self.dates.append(date)
        self.colour = self.getColour(self.group, self.height)
        self.new = True
        self.contents.append(content)

    def addEmpty(self, group, date):
        self.group = group
        self.height +=1
        self.colour = self.getColour(self.group, self.height)
        self.new = True
        if len(self.dates) < 7:
            self.dates.append(date)

    def delete(self):
        if self.height > 0:
            self.height -= 1
        self.pr_group = self.group
        if self.height == 0:
            self.group = None
            self.contents = []
        self.colour = self.getColour(self.group, self.height)
        self.removed = True
        self.dates[:-1]
        self.contents[:-1]

    def getColour(self, group, height):
        if group == None:
            return pygame.Color(255, 255, 255)
        h = height
        if h > 5:
            h = 5
        elif h <0:
            h = 0
        r = int(0.2 * h * colours[group.name][0] + (1 - (0.2 * h))*255)
        g = int(0.2 * h * colours[group.name][1] + (1 - (0.2 * h))*255)
        b = int(0.2 * h * colours[group.name][2] + (1 - (0.2 * h))*255)
        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        return pygame.Color(r, g, b)

class Stack:
    def __init__(self, name, kind, x, y):
        #print("stack " + str(name) +  " created")
        self.name = name
        self.kind = kind
        if self.kind == "empty":
            self.max = 17514
        else:
             self.max = 1290
        self.containers = []
        self.nr_groups = 0
        self.groupNrs = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.image = []
        self.x = x
        self.y = y
        if self.kind == "empty":
            for i in range(15):
                row = []
                for j in range(36):
                    row.append(ConPix())
                self.image.append(row)
        else:
            for i in range(28):
                self.image.append([ConPix(), ConPix(), ConPix(), ConPix(), ConPix(), ConPix(), ConPix(), ConPix(), ConPix(), ConPix()])


    def addContainer(self, container, date):
        self.groupNrs[container.group.name] += 1
        x = random.randint(0,len(self.image[0])-1)
        y = random.randint(0, len(self.image)-1)
        if container.empty:
            self.image[y][x].addEmpty(container.group, date)
        elif self.isFound(y, x, container):
            self.image[y][x].add(container.group, date, container.content)
            container.x = x
            container.y = y
        else:
            closest = self.findClosest(y, x, container)
            self.image[closest[0]][closest[1]].add(container.group, date, container.content)
            container.x = x
            container.y = y


    def removeContainer(self, container):
        self.groupNrs[container.group.name] -= 1
        self.image[container.y][container.x].delete()

    def findClosest(self, y, x, container):
        w = random.randint(0,len(self.image[0])-1)
        h = random.randint(0,len(self.image)-1)
        while not self.isFound(h,w,container):
            w = random.randint(0,len(self.image[0])-1)
            h = random.randint(0,len(self.image)-1)
        """print(str(h)+", "+ str(w))"""
        return [h,w]


    def isFound(self, h, w, container):
        #print(str(h) +", " + str(w))
        return (self.image[h][w].height < 6 and (self.image[h][w].group== container.group or self.image[h][w].group == None))
