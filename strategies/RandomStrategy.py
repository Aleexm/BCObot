import sys
sys.path.append("..")
from .Strategy import Strategy
import random

class RandomStrategy(Strategy):
    """Chooses uniformly random between all presented Options."""
    def __init__(self):
        self.name = "Random"
        super().__init__(self)

    def __repr__(self):
        return super().__repr__()

    def chooseOption(self, options, header=None):
        chosen_option = random.randint(1, len(options.keys()))
        return chosen_option
