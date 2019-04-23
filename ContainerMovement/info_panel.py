import time, random
from threading import Thread

class InfoPanel:
    def __init__(self, port, groups):
        self.port = port
        self.groups = groups

    def printDocks(self, int):
        if not self.port.docks[int].ship == None:
            return str(str(int) + ": " + str(len(self.port.docks[int].ship.containers)))
        else:
            return str(int) + ": X"

    def printStacks(self, int):
        for stack in self.port.ne_stacks:
            if stack.name == str(str(int)):
                return str(stack.name + ": Groups: " + str(stack.nr_groups) +
                ",   containers: " + str(len(stack.containers)))

    def printGroups(self, int):
        if self.groups[int].ship == None:
            return str(str(int) + ": containers: " + str(len(self.groups[int].containers)) +
            ",   " + self.groups[int].activity + ": dock None")
        else:
            return str(str(int) + ": containers: " + str(len(self.groups[int].containers)) +
            ",   " + self.groups[int].activity + ": dock " + str(self.groups[int].ship.dock.name))

    def give_info(self):
        while True:
            time.sleep(0.5)
            print("\n\n\n\n\n\n\n\n\nCurrent Status report:\n" + "Groups:\n")
            for i in range (len(self.groups)):
                print(self.printGroups(i))

            print("\nDocks:")

            for i in range(self.port.nr_docks):
                print(self.printDocks(i))

            print("\nNeStacks: ")
            for i in range(self.port.nr_non_empty_stacks):
                print(self.printStacks(i))

            print("\nEStack: " + str(len(self.port.e_stack.containers)))

            print ("\nShipQueue: " + str(len(self.port.ship_queue)))

            print ("\nTotal number of containers: " + str(self.port.nr_containers.counter))
