from Card import Card

class Pair:
    """Combines a played Style and Base into a Pair."""
    def __init__(self, base, style=None):
        # TODO: Finisher is awkward rn
        self.base = base
        self.style = style
        assert self.style is not None, "Missing a Style."
        assert self.base.type == Card.Type.base, "Base is not actually a Base."
        assert self.style.type == Card.Type.style, "Style is not actually a Style"
        properties_to_combine = ["attack", "priority", "defense", "min_range", "max_range", "soak", "start", "before", "hit", "on_hit", "after", "end"]
        for property in properties_to_combine:
            self.__dict__[property] = base.__dict__[property] + style.__dict__[property]

    def __repr__(self):
        return "({}, {}): Range:({}, {}), Atk: {}, Prio: {}, Def: {}".format(self.style, self.base, self.min_range, self.max_range, self.attack, self.priority, self.defense)
