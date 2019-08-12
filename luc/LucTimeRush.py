import sys
sys.path.append("..")
from Option import Option

class LucTimeRush:
    """Cost: 3 Time. Start: Advance up to 2."""
    def __init__(self):
        self.name = "Time Rush"
        self.user_info = "Cost: 3 Time. Start: Advance up to 2."
        self.unique = True # Can only ante once

    def __repr__(self):
        return self.name

    def apply(self, beat, players, active_player):
        """Adds the possiblity of advancing to the played pair, as that's when we'll decide."""
        players[active_player].time_tokens = max(players[active_player].time_tokens - 3, 0)
        beat.played_pairs[active_player].start.append(self.startAdvance)

    def startAdvance(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        """Either returns the possible advances as options ([Option]), or applies the chosen_option and advances."""
        p1 = players[active_player]
        if chosen_option is None:
            possible_moves = p1.getPossibleMoves([1,2], players, active_player)
            if len(possible_moves) > 0:
                options = []
                for move in possible_moves:
                    options.append(Option(name=self.name, user_info="Advance {}".format(move), params=move, function=self.startAdvance))
                return options
            return None
        else:
            p1.moveCharacter(chosen_option, players, active_player)
