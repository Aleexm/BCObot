class Board:
    '''
    Deprecated?
    '''
    players = None
    positions = None

    def __init__(self, players, positions):
        self.players = players
        self.positions = positions

    def moveCharacter(self, to_move, players, active_player):
        '''
        Moves the active player x squares.
        Arguments:
            to_move: (int) number of steps to move. (initially) Positive for advance, negative for retreat.
            active_player: (int) the active player who will be moving, 0 or 1.
        '''
        advance = True if to_move > 0 else False
        if self.positions[active_player] - self.positions[1-active_player] > 0:
            # advance is to the left (negative), retreat is to the right (positive)
            to_move = to_move*-1
        if advance and abs(to_move) >= abs(self.positions[1-active_player] - self.positions[active_player]):
            # You are moving past the opponent, increment move by 1.
            to_move = to_move+1 if to_move > 0 else to_move-1
        if self.positions[active_player] + to_move > 6 or self.positions[active_player] + to_move < 0:
            # Out of bounds
            print("can't move...")
        else:
            # We can move!
            new_position = self.positions[active_player] + to_move
            self.positions[active_player] = new_position
            self.players[active_player].position = new_position
            players[active_player].position = new_position
