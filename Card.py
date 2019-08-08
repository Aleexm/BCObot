from Board import Board
from enum import Enum

class Card:

    def __init__(self, name, type, attack, priority, defense, min_range, max_range=None, start = [], before = [], hit = [], after = [], end = []):
        self.name = name
        self.type = self.Type(type)
        self.min_range = min_range
        self.max_range = min_range if max_range is None else max_range
        self.attack = attack
        self.priority = priority
        self.defense = defense
        self.start = start
        self.before = before
        self.hit = hit
        self.after = after
        self.end = end

    def __repr__(self):
        return "{}: range: ({},{}), attack: {}, priority: {}, defense: {}".format(self.name, self.min_range, self.max_range, self.attack, self.priority, self.defense)
        # return self.name

    def executeActions(self, action_name, players, active_player):
        processed_cards = {}
        while True:
            added = False
            card_options = []
            for action in action_name:
                method = action[0]
                params = action[1:]
                if method not in processed_cards.keys():
                    options_to_add = method(*params, players, active_player)
                    if len(options_to_add) > 0:
                        added = True
                    card_options.append(options_to_add)
            if not added:
                break
            options = {}
            i = 1
            for option_list in card_options:
                for option in option_list:
                    options[i] = option
                    i+=1
            chosen_option = players[active_player].strategy.chooseOption(options)
            method = options[chosen_option][0]
            method(*params, players, active_player, chosen_option=options[chosen_option][3])
            processed_cards[method] = True

    class Type(Enum):
        base = 1
        style = 2
        finisher = 3
