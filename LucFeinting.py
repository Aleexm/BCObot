from Card import Card

class LucFeinting(Card):
    '''
    hi
    '''
    def __init__(self):
        super().__init__(name="Feinting", type=Card.Type.style, min_range=1, attack=1, priority=-2, defense=0, start=[[Card.moveCharacter], -1], end=[[self.end]])

    def __repr__(self):
        return super().__repr__()

    def end(self, players, active_player):
        "Advance 1 or 2."
        luc = players[active_player]
        possible_moves = luc.getPossibleMoves([1,2], players, active_player)
        options = {}
        for i, move in enumerate(possible_moves):
            options[i+1] = ["Advance", move]
        chosen_option = luc.strategy.chooseOption(options)
        luc.moveCharacter(chosen_option, players, active_player)
