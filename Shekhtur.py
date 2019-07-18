from Character import Character

class Shekhtur(Character):

    malice_tokens = None

    def __init__(self, position, cards, health):
        self.malice_tokens = 3
        super().__init__("Shekhtur", health=health, energy=2, position=position, cards = cards)

    def __repr__(self):
        return super().__repr__(additional_params = "Malice: {}".format(self.malice_tokens))