import time, random
from threading import Thread
from lorrys import Lorry
from ships import Ship

def getNrGroups(stack):
    return stack.nr_groups

class Group:
    speed = 1000
    def __init__(self, name, port, activity, nr_containers, colour):
        #print("Group " + str(name) +  " created")
        self.name = name
        self.port = port
        self.lowerBound = 1000
        self.upperBound = self.port.max_capacity
        self.max = random.randint(self.lowerBound, self.upperBound)
        self.containers = []
        self.stack = None
        self.activity = activity
        self.ship = None
        self.nr_containers = nr_containers
        self.colour = colour

    def findNeStack(self):
        stacks = self.port.ne_stacks
        stacks.sort(key = getNrGroups)
        for stack in stacks:
                if len(stack.containers) < stack.max:
                    stack.nr_groups = stack.nr_groups + 1
                    return stack

    def takeContainer(self, t):
        if len(self.containers) > 0:
            #print("containers in Group " + str(self.name) + " decreased")
            index = random.randint(0, len(self.containers)-1)
            container = self.containers[index]
            del self.containers[index]
            container.removeFromStack()
            time.sleep(2*(random.randint(1,t))/self.speed)
            return container

    def deliverContainer(self, container, t):
        if len(self.containers) < self.max:
            container.group = self
            #print("containers in Group " + str(self.name) + " increased")
            if container.empty:
                container.stack = self.port.e_stack
                container.putOnStack()
            else:
                if len(self.stack.containers) == self.stack.max:
                    self.stack.nr_groups = self.stack.nr_groups - 1
                    self.stack  = self.findNeStack()
                    if self.stack == None:
                        time.sleep(0.1)
                        self.stack = self.findNeStack()
                container.stack = self.stack
                container.putOnStack()
            self.containers.append(container)
            time.sleep(random.randint(1,t)/self.speed)

    def ask_ship(self):
        return self.port.ask_ship()

    def checkUnload(self):
        for d in self.port.docks:
            if d.occupied and len(self.port.ship_queue) > 0:
                return "inbound"
        else:
            return "outbound"

    def manageInbound(self):
        while len(self.port.ship_queue) == 0:
            time.sleep(1/self.speed)
        self.stack = self.findNeStack()
        self.ship = self.port.ship_queue.pop()
        self.ship.colour = self.colour
        self.max = len(self.ship.containers)
        self.ship.status = "arriving1"
        while not self.ship.status == "docked":
            time.sleep(1)
        while len(self.ship.containers) > 0:
            container = self.ship.containers.pop()
            self.deliverContainer(container, 10)
        self.ship = None
        lorry = Lorry(self)
        while len(self.containers) > 0:
            lorry.pickup_container(15)
        del lorry
        self.stack.nr_groups = self.stack.nr_groups - 1
        self.max = random.randint(self.lowerBound, self.upperBound)
        self.activity = self.checkUnload()

    def manageOutbound(self):
        dock = None
        lorry = Lorry(self)
        self.stack = self.findNeStack()
        while dock == None and len(self.containers) < self.max:
            dock = self.ask_ship()
            lorry.bring_container(15)
        while dock == None:
            dock = self.ask_ship()

        ship = Ship(dock, self.nr_containers, self.upperBound, self.port.emptyC)
        self.ship = ship
        ship.colour = self.colour
        self.port.ship_queue.append(ship)

        while len(self.containers) < self.max:
            lorry.bring_container(15)
        del lorry

        while not len(ship.containers) == 0:
            time.sleep(1/self.speed)
        ship.colour = self.colour
        self.ship = ship
        ship.status = "loading"
        while len(self.containers) > 0:
            ship.accept_container(self, 10)
        ship.status = "leaving1"
        while not ship.status == "left":
            time.sleep(0.1)
        del ship
        self.stack.nr_groups = self.stack.nr_groups - 1
        self.ship = None
        dock.ship = None
        dock.occupied = False
        self.max = random.randint(self.lowerBound, self.upperBound)
        self.activity = self.checkUnload()

    def manage(self):
        while True:
            self.upperBound = self.port.max_capacity
            if self.activity == "inbound":
                self.manageInbound()
            else:
                self.manageOutbound()
