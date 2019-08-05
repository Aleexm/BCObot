from Card import Card

class Pair:

    def __init__(self, base, style=None):
        self.base = base
        self.style = style
        if self.base.type == Card.Type.finisher:
            self.attack = base.attack
            self.priority = base.priority
            self.defense = base.defense
            self.min_range = base.min_range
            self.max_range = base.max_range
        else:
            assert self.style is not None, "Missing a Style."
            assert self.base.type == Card.Type.base, "Base is not actually a Base."
            assert self.style.type == Card.Type.style, "Style is not actually a Style"
            self.attack = base.attack + style.attack
            self.priority = base.priority + style.priority
            self.defense = base.priority = style.priority
            self.min_range = base.min_range + style.min_range
            self.max_range = base.max_range + style.max_range
