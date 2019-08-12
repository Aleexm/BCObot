from Card import Card
from Option import Option

class BaseDrive(Card):
    "Before: Advance 1 or 2 spaces."
    def __init__(self):
        super().__init__(name="Drive", type=Card.Type.base, attack=3, priority=4, defense=0, min_range=1, before=[self.beforeAdvance])

    def __repr__(self):
        return super().__repr__()

    def beforeAdvance(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        p1 = players[active_player]
        if chosen_option is None:
            possible_moves = p1.getPossibleMoves([1,2], players, active_player)
            if len(possible_moves) > 0:
                options = []
                for move in possible_moves:
                    options.append(Option(name=self.name, user_info="Advance {}".format(move), params=move, function=self.beforeAdvance))
                return options
            return None
        else:
            p1.moveCharacter(chosen_option, players, active_player)
