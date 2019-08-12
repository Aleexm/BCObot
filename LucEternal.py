from Card import Card
from Option import Option

class LucEternal(Card):
    """
    Soak 1. When you are hit, you may spend any amount of Time for Soak 1
    per Time spent.
    """
    def __init__(self):
        super().__init__(name="Eternal", type=Card.Type.style, min_range=0, attack=0, priority=-4, defense=0, soak=1, on_hit=[self.onHitSoak])

    def __repr__(self):
        return super().__repr__()

    def onHitSoak(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            if luc.time_tokens > 0:
                options = []
                options.append(Option(name=self.name, user_info="Do not spend Time Tokens.", params=0, function=self.onHitSoak))
                for i in range(1, min(luc.time_tokens+1, opp_pair.attack)):
                    options.append(Option(name=self.name, user_info="Spend {} Time Tokens for Soak {}.".format(i, i), params=i, function=self.onHitSoak))
                return options
            return None
        else:
            luc.time_tokens -= chosen_option
            my_pair.soak += chosen_option
