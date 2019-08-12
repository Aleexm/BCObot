from Card import Card
from Option import Option

class LucFeinting(Card):
    "Start: Retreat 1. End: Advance 1 or 2 spaces."

    def __init__(self):
        super().__init__(name="Feinting", type=Card.Type.style, min_range=1, attack=1, priority=-2, defense=0, start=[self.startRetreat], end=[self.endAdvance])

    def __repr__(self):
        return super().__repr__()

    def startRetreat(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            if len(luc.getPossibleMoves([-1], players, active_player)) > 0:
                options = [Option(name=self.name, user_info="Retreat 1", params=-1, function=self.startRetreat)]
                return options
            return None
        else:
            luc.moveCharacter(-1, players, active_player)

    def endAdvance(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            possible_moves = luc.getPossibleMoves([1,2], players, active_player)
            if len(possible_moves) > 0:
                options = []
                for move in possible_moves:
                    options.append(Option(name=self.name, user_info="Advance {}.".format(move), params=move, function=self.endAdvance))
                return options
            return None
        else:
            luc.moveCharacter(chosen_option, players, active_player)
