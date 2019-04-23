import time, random
from threading import Thread
from containers import Container

class Lorry:
    def __init__(self, group):
        self.group = group
        self.emptyC = self.group.port.emptyC

    def bring_container(self, t):
        #print("lorry brought a container to stack " + str(stack.name))
        container = Container(str(len(self.group.containers)), self.group, None, None, self.emptyC)
        self.group.nr_containers.incrCounter()
        self.group.deliverContainer(container, t)

    def pickup_container(self, t):
        self.group.takeContainer(t)
