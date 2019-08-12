from Card import Card
from Option import Option

class BaseStrike(Card):
    def __init__(self):
        super().__init__(name="Strike", type=Card.Type.base, attack=4, priority=3, defense=5, min_range=1)

    def __repr__(self):
        return super().__repr__()
