import time, random
from threading import Thread

incomingContents = ["Machinery", "Electronics", "Toys", "Furniture", "Footwear", "Plastics", "Clothing", "Leather", "Iron", "Knit"]
outboundContents = ["Aluminium", "Medicine", "Minerals", "Orange", "Nuts", "Fish", "Yoghurt", "Eggs", "Olives", "Marble" ]

class totContainers:
    def __init__(self):
        self.counter = 0

    def incrCounter(self):
        self.counter = self.counter + 1

class Container:
    """docstring for ."""
    def __init__(self, name, group, stack, ship, emptyC):
        #super(Container, self).__init__()
        self.name = name
        eInt = random.randint(1,100)
        if eInt < emptyC:
            self.empty = True
        else:
            self.empty = False
        self.group = group
        self.stack = stack
        self.ship = ship
        self.x = 0
        self.y = 0
        self.content = self.addContent()

    def putOnStack(self):
        self.stack.containers.append(self)
        self.stack.addContainer(self, self.group.port.date)

    def addContent(self):
        int = random.randint(0, 9)
        if not self.ship == None:
            return incomingContents[int]
        else:
            return outboundContents[int]

    def removeFromStack(self):
        self.stack.containers.remove(self)
        self.stack.removeContainer(self)
