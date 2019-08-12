from Card import Card
from Option import Option
import numpy as np

class BaseGrasp(Card):
    """Hit: Push or Pull the opponent 1 space."""
    def __init__(self):
        super().__init__(name="Grasp", type=Card.Type.base, attack=2, priority=5, defense=0, min_range=1, hit=[self.pushPull])

    def __repr__(self):
        return super().__repr__()

    def pushPull(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        """Either returns the possible push/pull as options ([Option]), or applies the chosen_option and pushes/pulls."""
        luc = players[active_player]
        luc.static_effects[luc.StaticEffects.ignore_stun_guard] = True
        enemy = players[1-active_player]
        if chosen_option is None:
            possible_moves = np.multiply(enemy.getPossibleMoves([-1, 1], players, 1-active_player), -1)
            options = []
            if len(possible_moves) > 0:
                for i, move in enumerate(possible_moves):
                    if move > 0:
                        string = "Push"
                    else:
                        string = "Pull"
                    options.append(Option(name=self.name, user_info="{} {}".format(string, 1), params=move, function=self.pushPull))
                return options
            return None
        else: # TODO: Can't be moved opponent functionality
            enemy.moveCharacter(chosen_option*-1, players, 1-active_player)
