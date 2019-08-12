from Card import Card
from Option import Option

class BaseBurst(Card):
    "Start: Retreat 1 or 2 spaces."
    def __init__(self):
        super().__init__(name="Burst", type=Card.Type.base, attack=3, priority=1, defense=0, min_range=2, max_range=3, start=[self.startRetreat])

    def __repr__(self):
        return super().__repr__()

    def startRetreat(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        p1 = players[active_player]
        if chosen_option is None:
            possible_moves = p1.getPossibleMoves([-1,-2], players, active_player)
            if len(possible_moves) > 0:
                options = []
                for move in possible_moves:
                    options.append(Option(name=self.name, user_info="Retreat {}".format(move*-1), params=move, function=self.startRetreat))
                return options
            return None
        else:
            p1.moveCharacter(chosen_option, players, active_player)
