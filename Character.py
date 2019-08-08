from Strategy import Strategy
from copy import deepcopy

class Character:

    name = None
    health = None
    energy = None
    position = None
    cards_hand = None
    cards_discard = None
    strategy = None

    def __init__(self, name, health, energy, position, strategy, cards_hand, cards_discard=None):
        self.name = name
        self.health = health
        self.energy = energy
        self.position = position
        self.cards_hand = cards_hand
        self.cards_discard = cards_discard
        self.strategy = strategy

    def __repr__(self, additional_params):
        return "Character: {}, Health: {}, Energy: {}, Position: {}, cards: {}, {}".format(
               self.name, self.health, self.energy, self.position, self.cards_hand, additional_params)

    def getPossibleMoves(self, moves_list, players, active_player):
        p1 = self
        p2 = players[1-active_player]
        possible_moves = []
        for move in moves_list:
            to_move = deepcopy(move)
            advance = True if to_move > 0 else False
            if p1.position - p2.position > 0:
                # advance is to the left (negative), retreat is to the right (positive)
                to_move = to_move*-1
            if advance and abs(to_move) >= abs(p2.position - p1.position):
                # You are moving past the opponent, increment move by 1.
                to_move = to_move+1 if to_move > 0 else to_move-1
            if p1.position + to_move <= 6 and p1.position + to_move >= 0:
                possible_moves.append(move)
        return possible_moves
        
    def moveCharacter(self, to_move, players, active_player):
        '''
        Moves the active player x squares.
        Arguments:
            to_move: (int) number of steps to move. (initially) Positive for advance, negative for retreat.
            players: (list of class Character) [p1, p2].
            active_player: (int) the active player who will be moving, 0 or 1.
        '''
        p1 = players[active_player]
        p2 = players[1-active_player]
        advance = True if to_move > 0 else False
        if  p1.position - p2.position > 0:
            # advance is to the left (negative), retreat is to the right (positive)
            to_move = to_move*-1
        if advance and abs(to_move) >= abs(p2.position - p1.position):
            # You are moving past the opponent, increment move by 1.
            to_move = to_move+1 if to_move > 0 else to_move-1
        if  p1.position + to_move > 6 or p1.position + to_move < 0:
            # Out of bounds
            print("can't move...")
        else:
            # We can move!
            new_position = p1.position + to_move
            p1.position = new_position
            
    # def choicePlayer(self, options):


    # def openingHand(self, cards_hand):
