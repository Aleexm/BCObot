from Card import Card

class LucChrono(Card):
    "Start: Spend up to 3 Time Tokens to close that many spaces."

    def __init__(self):
        super().__init__(name="Chrono", type=Card.Type.style, attack=0, priority=1, defense=0, min_range=0, start=[self.close])

    def __repr__(self):
        return super().__repr__()

    def close(self, players, active_player, my_pair, chosen_option=None):
        luc = players[active_player]
        enemy = players[1-active_player]
        if chosen_option is None:
            time_tokens = luc.time_tokens
            if time_tokens == 0:
                return None # Can't advance
            possible_close = min(abs(luc.position - enemy.position) - 1, time_tokens, 3)
            if possible_close == 0:
                return None # Already next to enemy
            options = []
            options.append([self.close, "({})".format(self.name), "Do not advance.", 0])
            for move in range(1, possible_close+1):
                options.append([self.close, "({})".format(self.name), "Advance {}.".format(move), move])
            return options
        else:
            luc.moveCharacter(to_move=chosen_option, players=players, active_player=active_player)
            luc.time_tokens -= chosen_option
