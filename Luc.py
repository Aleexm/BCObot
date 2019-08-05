from Character import Character

class Luc(Character):

    time_tokens = None

    def __init__(self, position, cards_hand, strategy, health):
        self.time_tokens = 2
        super().__init__("Luc", health=health, energy=2, position=position, strategy=strategy, cards_hand=cards_hand)

    def __repr__(self):
        return super().__repr__(additional_params = "Time: {}".format(self.time_tokens))

    def createCards(self):
        pass
        # chrono = Card("Chrono", type=Card.Type.style, min_range=0, attack=0, priority=1, defense=0, start)
