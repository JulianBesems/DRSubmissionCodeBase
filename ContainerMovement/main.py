import time, random, datetime, pygame
from threading import Thread
from port import Port
from groups import Group
from info_panel import InfoPanel
from containers import totContainers
from container_movement_graphics import Graphics

class PortLogic:
    def __init__(self):
        self.time = datetime.datetime.now()

    def logic(self):
        nr_containers = totContainers()
        port = Port("PiraeusPier2", nr_containers)
        threads = []
        groups = []
        nr_groups = 13
        colours = []
        colours.append(pygame.Color(228, 197, 73))
        colours.append(pygame.Color(185, 0, 37))
        colours.append(pygame.Color(78, 87, 111))
        colours.append(pygame.Color(12, 63, 50))
        colours.append(pygame.Color(236, 110, 0))
        colours.append(pygame.Color(68, 22, 33))
        colours.append(pygame.Color(143, 149, 160))
        colours.append(pygame.Color(185, 197, 201))
        colours.append(pygame.Color(35, 127, 125))
        colours.append(pygame.Color(149, 132, 103))
        colours.append(pygame.Color(0, 44, 125))
        colours.append(pygame.Color(0, 160, 213))
        colours.append(pygame.Color(166, 202, 87))
        colours.append(pygame.Color(228, 166, 156))

        for i in range(nr_groups - port.nr_docks):
            groups.append(Group(i, port, "outbound", nr_containers, colours[i]))
        for i in range(nr_groups - port.nr_docks, nr_groups):
            groups.append(Group(i, port, "inbound", nr_containers, colours[i]))
        info = InfoPanel(port, groups)
        for i in range(nr_groups):
            thread = Thread(target = groups[i].manage, name = str(i), daemon = True)
            threads.append(thread)
        """info = Thread(target = info.give_info, name = str(nr_groups + 1), daemon = True)
        threads.append(info)"""
        for t in threads:
            t.start()
        graphics = Graphics(port, groups)
        graphics.display()
        while True:
            pass


logic = PortLogic()
logic.logic()
