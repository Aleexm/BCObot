from Card import Card

class LucFeinting(Card):
    "Start: Retreat 1. End: Advance 1 or 2 spaces."

    def __init__(self):
        super().__init__(name="Feinting", type=Card.Type.style, min_range=1, attack=1, priority=-2, defense=0, start=[self.startRetreat], end=[self.endAdvance])

    def __repr__(self):
        return super().__repr__()

    def startRetreat(self, players, active_player, my_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            if len(luc.getPossibleMoves([-1], players, active_player)) > 0:
                options = [[self.startRetreat, "({})".format(self.name), "Retreat 1", -1]]
            else:
                options = None
            return options
        else:
            luc.moveCharacter(-1, players, active_player)

    def endAdvance(self, players, active_player, my_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            possible_moves = luc.getPossibleMoves([1,2], players, active_player)
            if len(possible_moves) > 0:
                options = []
                for move in possible_moves:
                    options.append([self.endAdvance, "({})".format(self.name), "Advance {}".format(move), move])
                return options
            else:
                return None
        else:
            luc.moveCharacter(chosen_option, players, active_player)
