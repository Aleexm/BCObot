from Strategy import Strategy

class Character:

    name = None
    health = None
    energy = None
    position = None
    cards_hand = None
    cards_discard = None
    strategy = None

    def __init__(self, name, health, energy, position, strategy, cards_hand, cards_discard=None):
        self.name = name
        self.health = health
        self.energy = energy
        self.position = position
        self.cards_hand = cards_hand
        self.cards_discard = cards_discard
        self.strategy = strategy

    def __repr__(self, additional_params):
        return "Character: {}, Health: {}, Energy: {}, Position: {}, cards: {}, {}".format(
               self.name, self.health, self.energy, self.position, self.cards_hand, additional_params)

    # def choicePlayer(self, options):


    # def openingHand(self, cards_hand):
