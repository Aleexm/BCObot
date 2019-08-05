class Pair:

    def __init__(self, base, style):
        self.base = base,
        self.style = style
        self.attack = base.attack + style.attack
        self.priority = base.priority + style.priority
        self.defense = base.priority = style.priority
        self.range = (base.min_range + style.min_range, base.max_range + style.max_range)
