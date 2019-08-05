from Strategy import Strategy
import random

class RandomStrategy(Strategy):

    def __init__(self):
        self.name = "Random"
        super().__init__(self)

    def __repr__(self):
        return super().__repr__()

    def chooseOption(self, options):
        chosen_option = random.randint(0, len(options.keys())-1)
        return chosen_option
