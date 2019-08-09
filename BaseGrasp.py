from Card import Card

class BaseGrasp(Card):
    def __init__(self):
        super().__init__(name="Grasp", type=Card.Type.base, attack=2, priority=5, defense=0, min_range=1, hit=[self.pushPull])

    def __repr__(self):
        return super().__repr__()

    def pushPull(self, players, active_player, my_pair, chosen_option=None):
        "Hit: Push or Pull the opponent 1 space."
        luc = players[active_player]
        enemy = players[1-active_player]
        if chosen_option is None:
            possible_moves = enemy.getPossibleMoves([-1, 1], players, 1-active_player)
            options = []
            for i, move in enumerate(possible_moves):
                if move > 0:
                    string = "Pull"
                else:
                    string = "Push"
                options.append([self.pushPull, "({})".format(self.name), "{} {}.".format(string, 1), move*-1])
            return options
        else:
            enemy.moveCharacter(chosen_option*-1, players, 1-active_player)
