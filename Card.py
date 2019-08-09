from Board import Board
from enum import Enum

class Card:

    def __init__(self, name, type, attack, priority, defense, min_range, max_range=None, soak=0, start = [], before = [], hit = [], on_hit=[], after = [], end = []):
        self.name = name
        self.type = self.Type(type)
        self.min_range = min_range
        self.max_range = min_range if max_range is None else max_range
        self.attack = attack
        self.priority = priority
        self.defense = defense
        self.soak = soak
        self.start = start
        self.before = before
        self.hit = hit
        self.on_hit = on_hit
        self.after = after
        self.end = end

    def __repr__(self):
        return "{}: range: ({},{}), attack: {}, priority: {}, defense: {}".format(self.name, self.min_range, self.max_range, self.attack, self.priority, self.defense)
        # return self.name

    class Type(Enum):
        base = 1
        style = 2
        finisher = 3
