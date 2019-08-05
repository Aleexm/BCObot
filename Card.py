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
        return "{}: range: ({},{}), attack: {}, priority: {}, defense: {}".format(self.name, self.min_range, self.max_range, self.attack, self.priority, self.defense)
        # return self.name

    def executeActions(self, action_name, players, active_player):
        for action in action_name:
            method = action[0]
            params = action[1:]
            method(*params, players, active_player)
            # Chrono.start(players, active_player)

    def moveCharacter(self, to_move, players, active_player):
        '''
        Moves the active player x squares.
        Arguments:
            to_move: (int) number of steps to move. (initially) Positive for advance, negative for retreat.
            active_player: (int) the active player who will be moving, 0 or 1.
        '''
        advance = True if to_move > 0 else False
        if players[active_player].position - players[1-active_player].position > 0:
            # advance is to the left (negative), retreat is to the right (positive)
            to_move = to_move*-1
        if advance and abs(to_move) >= abs(players[1-active_player].position - players[active_player].position):
            # You are moving past the opponent, increment move by 1.
            to_move = to_move+1 if to_move > 0 else to_move-1
        if players[active_player].position + to_move > 6 or players[active_player].position + to_move < 0:
            # Out of bounds
            print("can't move...")
        else:
            # We can move!
            new_position = players[active_player].position + to_move
            players[active_player].position = new_position


    class Type(Enum):
        base = 1
        style = 2
        finisher = 3
