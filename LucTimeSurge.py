class LucTimeSurge:
    def __init__(self):
        self.name = "Time Surge"
        self.user_info = "Cost: 1 Time. +1 Priority."
        self.unique = True # Can only ante once

    def __repr__(self):
        return self.name

    def apply(self, beat, players, active_player):
        """Increments the played pair's priority by 1."""
        players[active_player].time_tokens = max(players[active_player].time_tokens - 1, 0)
        beat.played_pairs[active_player].priority += 1
