from Character import Character

class Luc(Character):

    time_tokens = None

    def __init__(self, position, cards, health):
        self.time_tokens = 2
        super().__init__("Luc", health=health, energy=2, position=position, cards = cards)

    def __repr__(self):
        return super().__repr__(additional_params = "Time: {}".format(self.time_tokens))
