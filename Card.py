from Board import Board
class Card:

    name = None
    range = None # TODO : Min/max range
    attack = None
    priority = None
    defense = None
    start = None
    before = None
    after = None

    def __init__(self, name, range, attack, priority, defense, start = [], before = [], after = []):
        self.name = name
        self.range = range
        self.attack = attack
        self.priority = priority
        self.defense = defense
        self.start = start
        self.before = before
        self.after = after

    def __repr__(self):
        # return "{}: range: {}, attack: {}, priority: {}, defense: {}".format(self.name, self.range, self.attack, self.priority, self.defense)
        return self.name

    def executeActions(self, action_name, players, active_player):
        for action in action_name:
            method = action[0]
            params = action[1:]
            method(*params, active_player)
            # action(active_player)

    # def moveCharacter(to_move, players, active_player):







# card = Card("Memento", 0, 0, 1, 0)
