class Card:

    name = None
    range = None # TODO : Min/max range
    attack = None
    priority = None
    defense = None

    def __init__(self, name, range, attack, priority, defense):
        self.name = name
        self.range = range
        self.attack = attack
        self.priority = priority
        self.defense = defense

    def __repr__(self):
        # return "{}: range: {}, attack: {}, priority: {}, defense: {}".format(self.name, self.range, self.attack, self.priority, self.defense)
        return self.name



# card = Card("Memento", 0, 0, 1, 0)
