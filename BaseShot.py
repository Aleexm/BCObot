from Card import Card
from Option import Option

class BaseShot(Card):
    def __init__(self):
        super().__init__(name="Shot", type=Card.Type.base, attack=3, priority=2, defense=2, min_range=1, max_range=4)

    def __repr__(self):
        return super().__repr__()
