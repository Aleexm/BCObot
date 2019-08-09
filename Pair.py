from Card import Card

class Pair:

    def __init__(self, base, style=None):
        self.base = base
        self.style = style
        if self.base.type == Card.Type.finisher:
            self.attack = base.attack
            self.priority = base.priority
            self.defense = base.defense
            self.min_range = base.min_range
            self.max_range = base.max_range
        else:
            assert self.style is not None, "Missing a Style."
            assert self.base.type == Card.Type.base, "Base is not actually a Base."
            assert self.style.type == Card.Type.style, "Style is not actually a Style"
            self.attack = base.attack + style.attack
            self.priority = base.priority + style.priority
            self.defense = base.priority = style.priority
            self.min_range = base.min_range + style.min_range
            self.max_range = base.max_range + style.max_range
            self.soak = base.soak + style.soak
            self.start = [item for sublist in [self.base.start, self.style.start] for item in sublist]
            self.before = [item for sublist in [self.base.before, self.style.before] for item in sublist]
            self.hit = [item for sublist in [self.base.hit, self.style.hit] for item in sublist]
            self.on_hit = [item for sublist in [self.base.on_hit, self.style.on_hit] for item in sublist]
            self.after = [item for sublist in [self.base.after, self.style.after] for item in sublist]
            self.end = [item for sublist in [self.base.end, self.style.end] for item in sublist]

    def executeActions(self, action_name, players, active_player):
        processed_cards = {}
        while True:
            added = False
            card_options = []
            for action in action_name:
                method = action
                if method not in processed_cards.keys():
                    options_to_add = method(players, active_player, self)
                    if options_to_add is not None:
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
            method(players, active_player, self, chosen_option=options[chosen_option][3])
            processed_cards[method] = True
