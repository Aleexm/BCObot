import sys
sys.path.append("..")
from Card import Card
from Option import Option

class LucChrono(Card):
    """Start: Spend up to 3 Time Tokens to close that many spaces."""
    def __init__(self):
        super().__init__(name="Chrono", type=Card.Type.style, attack=0, priority=1, defense=0, min_range=0, start=[self.close])

    def __repr__(self):
        return super().__repr__()

    def close(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        """Either returns the possible closes as options ([Option]), or applies the chosen_option and closes."""
        luc = players[active_player]
        enemy = players[1-active_player]
        if chosen_option is None:
            time_tokens = luc.time_tokens
            possible_moves = luc.getPossibleMoves([i+1 for i in range(min(abs(luc.position - enemy.position) - 1, time_tokens, 3))], players, active_player)
            if len(possible_moves) > 0:
                options = []
                options.append(Option(name=self.name, user_info="Do not advance.", params=0, function=self.close))
                for move in possible_moves:
                    options.append(Option(name=self.name, user_info="Spend {} time to advance {}.".format(move, move), params=move, function=self.close))
                return options
            return None
        else:
            luc.moveCharacter(to_move=chosen_option, players=players, active_player=active_player)
            luc.time_tokens -= chosen_option
