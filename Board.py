class Board:
    players = None
    positions = None

    def __init__(self, players, positions):
        self.players = players
        self.positions = positions

    def moveCharacter(self, to_move, active_player):
        advance = True if to_move > 0 else False
        if self.positions[active_player] - self.positions[1-active_player] > 0:
            # advance is to the left (negative), retreat is to the right (positive)
            to_move = to_move*-1
        if advance and abs(to_move) >= abs(self.positions[1-active_player] - self.positions[active_player]):
            to_move = to_move+1 if to_move > 0 else to_move-1
        if self.positions[active_player] + to_move > 6 or self.positions[active_player] + to_move < 0:
            print("can't move...")
        else:
            new_position = self.positions[active_player] + to_move
            self.positions[active_player] = new_position
            self.players[active_player].position = new_position
