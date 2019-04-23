import time, random
from threading import Thread
from docks import Dock
from stacks import Stack

class Port:
    def __init__(self, name, nr_containers):
        #print("port created")
        self.ship_queue = []
        self.docks = []
        self.ne_stacks = []
        self.name = name
        self.nr_docks = 7
        self.nr_non_empty_stacks = 16
        self.max_capacity = 3000
        for i in range(self.nr_docks):
            self.docks.append(Dock(i))
        for i in range(8):
            self.ne_stacks.append(Stack(str(str(i)), "non empty", i, 0))
        for i in range(8, 16):
            self.ne_stacks.append(Stack(str(str(i)), "non empty", i - 8, 1))
        self.e_stack = Stack(str("E"), "empty", 0, 0)
        self.nr_containers = nr_containers
        self.date = 0
        self.emptyC = 20

    def __str__(self):
        return str(self.name)

    def ask_ship(self):
        for i in self.docks:
            if not i.occupied:
                i.occupied = True
                #print("dock " + str(i.name) + "is occupied")
                return i
        return None
