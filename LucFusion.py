from Card import Card
from Option import Option

class LucFusion(Card):
    """
    Hit: Push the oppponent 1 or 2 spaces.
    Hit: If the opponent is at the edge of the board, they lose 2 life.
    """

    def __init__(self):
        super().__init__(name="Fusion", type=Card.Type.style, min_range=0, attack=0, priority=1, defense=0, hit=[self.push, self.damage])

    def __repr__(self):
        return super().__repr__()

    def push(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        luc = players[active_player]
        p2 = players[1-active_player]
        if chosen_option is None:
            possible_pushes = p2.getPossibleMoves([-1, -2], players, 1-active_player)
            if len(possible_pushes) > 0:
                options = []
                for i, move in enumerate(possible_pushes):
                    options.append(Option(name="{} 1".format(self.name), user_info="Push {}.".format(move*-1), params=move*-1, function=self.push))
                return options
            return None
        else:
            p2.moveCharacter(chosen_option*-1, players, 1-active_player)

    def damage(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        if chosen_option is None:
            if players[1-active_player].position == 0 or players[1-active_player].position == 6:
                options = []
                options.append(Option(name="{} 2".format(self.name),
                user_info="If the opponent is at the edge of the board, they lose 2 life.", params=0, function=self.damage))
                return options
            return None
        else:
            opp_pos = players[1-active_player].position
            if opp_pos == 0 or opp_pos == 6:
                players[1-active_player].health = max(players[1-active_player].health - 2, 1)
