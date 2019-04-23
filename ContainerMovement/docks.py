import time, random
from threading import Thread

class Dock:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.ship = None
