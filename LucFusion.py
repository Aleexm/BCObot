from Card import Card

class LucFusion(Card):
    "Contains all functionality for Luc's Fusion style."

    def __init__(self):
        super().__init__(name="Fusion", type=Card.Type.style, min_range=0, attack=0, priority=1, defense=0, hit=[self.push, self.damage])

    def __repr__(self):
        return super().__repr__()

    def push(self, players, active_player, my_pair, chosen_option=None):
        "Hit: Push the opponent 1 or 2 spaces."
        luc = players[active_player]
        p2 = players[1-active_player]
        if chosen_option is None:
            possible_pushes = p2.getPossibleMoves([-1, -2], players, 1-active_player)
            options = []
            for i, move in enumerate(possible_pushes):
                options.append([self.push, "({} 1)".format(self.name), "Push {}.".format(move*-1), move*-1])
            return options
        else:
            p2.moveCharacter(chosen_option*-1, players, 1-active_player)

    def damage(self, players, active_player, my_pair, chosen_option=None):
        "Hit: If the opponent is at the edge of the board, they lose 2 life."
        if chosen_option is None:
            options = [[self.damage, "({} 2)".format(self.name), "If the opponent is at the edge of the board, they lose 2 life.", 0]]
            return options
        else:
            opp_pos = players[1-active_player].position
            if opp_pos == 0 or opp_pos == 6:
                players[1-active_player].health -= 2
