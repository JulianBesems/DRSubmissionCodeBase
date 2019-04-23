import time, random
from threading import Thread

class Ship:
    def __init__(self, dock):
        print("new ship arrived at dock " + str(dock.name) + '\n')
        self.counter = 0
        self.max = 9
        dock.ship = self

    def accept_container(self, stack):
        while self.counter < self.max:
            #print("ship accepted container from stack " + str(stack.name))
            self.counter += 1
            stack.decrease()

    def is_full(self):
        return self.counter == self.max


class Stack:
    def __init__(self, name, port):
        #print("stack " + str(name) +  " created")
        self.name = name
        self.counter = 0
        self.max = 9
        self.port = port

    def decrease(self):
        if self.counter > 0:
            #print("containers in stack " + str(self.name) + " decreased")
            self.counter -= 1
            time.sleep(random.randint(1,2))

    def increase(self):
        if self.counter < self.max:
            #print("containers in stack " + str(self.name) + " increased")
            self.counter += 1
            time.sleep(random.randint(1,3))

    def ask_ship(self):
        return self.port.ask_ship()

    def manage(self):
        while True:
            if self.counter == 0:
                lorry = Lorry()
                while self.counter < self.max:
                    lorry.bring_container(self)
                del lorry
            elif self.counter == self.max:
                dock = self.ask_ship()
                ship = Ship(dock)
                while self.counter > 0:
                    ship.accept_container(self)
                if ship.is_full():
                    del ship
                dock.ship = None
                dock.occupied = False
                #print("dock " + str(dock.name) + "is free")

class Lorry:
    def bring_container(self, stack):
        #print("lorry brought a container to stack " + str(stack.name))
        stack.increase()

class Port:
    def __init__(self):
        #print("port created")
        self.ship_queue = []
        self.docks = []
        for i in range(3):
            self.docks.append(Dock(i))

    def ask_ship(self):
        while True:
            for i in self.docks:
                if not i.occupied:
                    i.occupied = True
                    #print("dock " + str(i.name) + "is occupied")
                    return i

class Dock:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.ship = None

class InfoPanel:
    def __init__(self, port, stacks):
        self.port = port
        self.stacks = stacks

    def give_info(self):
        while True:
            time.sleep(2)
            print("Current Status report:\n" +
                  "Stacks:\n" +
                  "1:  " + str(self.stacks[0].counter) + "\t, 2:  " + str(self.stacks[1].counter) + "\t, 3:  " + str(self.stacks[2].counter) + "\t, 4:  " + str(self.stacks[3].counter) + '\n' +
                  "5:  " + str(self.stacks[4].counter) + "\t, 6:  " + str(self.stacks[5].counter) + "\t, 7:  " + str(self.stacks[6].counter) + "\t, 8:  " + str(self.stacks[7].counter) + '\n' +
                  "9:  " + str(self.stacks[8].counter) + "\t, 10: " + str(self.stacks[9].counter) + "\n \n"+
                  "Ports:\n" +
                  "1: ")
            if self.port.docks[0].occupied:
                print(str(self.port.docks[0].ship.counter) + '\n')
            else:
                print("X\n")
            print("2: ")
            if self.port.docks[1].occupied:
                print(str(self.port.docks[0].ship.counter) + '\n')
            else:
                print("X \n")
            print("3: ")
            if self.port.docks[1].occupied:
                print(str(self.port.docks[0].ship.counter) + '\n')
            else:
                print("X \n")



if __name__ == "__main__":
    port = Port()
    threads = []
    stacks = []
    for i in range(10):
        stacks.append(Stack(i, port))
    info = InfoPanel(port, stacks)
    for i in range(10):
        thread = Thread(target = stacks[i].manage, name = str(i), daemon = True)
        threads.append(thread)
    info = Thread(target = info.give_info, name = str(11), daemon = True)
    threads.append(info)
    for t in threads:
        t.start()
    while True:
        pass
