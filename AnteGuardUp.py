class AnteGuardUp:
    def __init__(self):
        self.name = "Guard Up"
        self.user_info = "+2 Guard."

    def __repr__(self):
        return self.name

    def apply(self, beat, players, active_player):
        players[active_player].force = max(players[active_player].force - 2, 0)
        beat.played_pairs[active_player].defense += 2
