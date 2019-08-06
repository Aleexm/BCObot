from Card import Card

class LucChrono(Card):
    def __init__(self):
        super().__init__(name="Chrono", type=Card.Type.style, attack=0, priority=1, defense=0, min_range=0, start=[[self.start]])

    def __repr__(self):
        return super().__repr__()

    def start(self, players, active_player):
        "Spend up to 3 Time Tokens to close that many spaces."
        luc = players[active_player]
        enemy = players[1-active_player]
        time_tokens = luc.time_tokens
        if time_tokens == 0:
            return # Can't advance
        possible_close = min(abs(luc.position - enemy.position) - 1, time_tokens, 3)
        if possible_close == 0:
            return # Already next to enemy
        options = {}
        for i in range(1, possible_close+2):
            options[i] = "Advance {}".format(i-1) # User's options are 1 based because not everyone is a programmer... smh
        chosen_option = luc.strategy.chooseOption(options = options) - 1
        self.moveCharacter(to_move=chosen_option, players=players, active_player=active_player)
        luc.time_tokens -= chosen_option
