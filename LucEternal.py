from Card import Card

class LucEternal(Card):
    """
    Soak 1. When you are hit, you may spend any amount of Time for Soak 1
    per Time spent.
    """
    def __init__(self):
        super().__init__(name="Eternal", type=Card.Type.style, min_range=0, attack=0, priority=-4, defense=0, soak=1, on_hit=[self.onHitSoak])

    def __repr__(self):
        return super().__repr__()

    def onHitSoak(self, players, active_player, my_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            if luc.time_tokens > 0:
                options = []
                options.append([self.onHitSoak, "({})".format(self.name), "Do not spend Time Tokens.", 0])
                for i in range(1, luc.time_tokens+1):
                    options.append([self.onHitSoak, "({})".format(self.name), "spend {} Time Tokens for Soak {}.".format(i, i), i])
                return options
            return None
        else:
            my_pair.soak += chosen_option
