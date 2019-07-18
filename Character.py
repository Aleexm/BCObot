class Character:

    name = None
    health = None
    energy = None
    position = None
    cards = None

    def __init__(self, name, health, energy, position, cards):
        self.name = name
        self.health = health
        self.energy = energy
        self.position = position
        self.cards = cards

    def __repr__(self, additional_params):
        return "Character: {}, Health: {}, Energy: {}, Position: {}, cards: {}, {}".format(
               self.name, self.health, self.energy, self.position, self.cards, additional_params)
