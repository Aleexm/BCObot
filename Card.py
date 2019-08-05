from Board import Board
from enum import Enum

class Card:

    def __init__(self, name, type, attack, priority, defense, min_range, max_range=None, start = [], before = [], after = [], end = []):
        self.name = name
        self.type = self.Type(type)
        self.min_range = min_range
        self.max_range = min_range if max_range is None else max_range
        self.attack = attack
        self.priority = priority
        self.defense = defense
        self.start = start
        self.before = before
        self.after = after
        self.end = end

    def __repr__(self):
        # return "{}: range: {}, attack: {}, priority: {}, defense: {}".format(self.name, self.range, self.attack, self.priority, self.defense)
        return self.name

    def executeActions(self, action_name, players, active_player):
        for action in action_name:
            method = action[0]
            params = action[1:]
            method(*params, active_player)
            # action(active_player)

    class Type(Enum):
        base = 1
        style = 2
        finisher = 3
