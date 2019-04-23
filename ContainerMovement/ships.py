import time, random
from threading import Thread
from containers import Container

class Ship:
    def __init__(self, dock, nr_containers, max_capacity, emptyC):
        #print("new ship arrived at dock " + str(dock.name) + '\n')
        self.containers = []
        self.nr_containers = nr_containers
        self.dock = dock
        self.status = "queing"
        dock.ship = self
        self.colour = None
        self.max_capacity = max_capacity
        self.emptyC = emptyC
        self.containers = self.fillContainers()


    def fillContainers(self):
        containers = []
        rand = random.randint(1000, self.max_capacity)
        for i in range(rand):
            container = Container(i, None, None, self, self.emptyC)
            containers.append(container)
            self.nr_containers.incrCounter()
        return containers

    def accept_container(self, group, t):
        while len(group.containers) > 0:
            #print("ship accepted container from stack " + str(stack.name))
            self.containers.append(group.takeContainer(t))
