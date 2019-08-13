class AntePowerUp:
    def __init__(self):
        self.name = "Power Up"
        self.user_info = "+1 Power."

    def __repr__(self):
        return self.name

    def payCost(self, beat, players, active_player):
        players[active_player].force = max(players[active_player].force - 2, 0)

    def apply(self, beat, players, active_player):
        beat.played_pairs[active_player].attack += 1
