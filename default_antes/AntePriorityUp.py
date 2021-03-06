class AntePriorityUp:
    def __init__(self):
        self.name = "Priority Up"
        self.user_info = "+2 Priority."

    def __repr__(self):
        return self.name

    def payCost(self, beat, players, active_player):
        players[active_player].force = max(players[active_player].force - 2, 0)

    def apply(self, beat, players, active_player):
        beat.played_pairs[active_player].priority += 2
