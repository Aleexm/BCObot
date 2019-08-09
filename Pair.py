from Card import Card

class Pair:

    def __init__(self, base, style=None):
        # TODO: Finisher is awkward rn
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
            properties_to_combine = ["attack", "priority", "defense", "min_range", "max_range", "soak", "start", "before", "hit", "on_hit", "after", "end"]
            for property in properties_to_combine:
                self.__dict__[property] = base.__dict__[property] + style.__dict__[property]

    # TODO: This can't really be in Pair as it's impossible to detect opposing "can't be moved" for example
    def executeActions(self, action_name, players, active_player):
        processed_cards = {} # dict containing cards whose actions we've executed
        while True:
            added = False # Boolean to check whether any actions remain
            card_options = []
            for action in action_name: # action is a function object, i.e. chrono.close
                if action not in processed_cards.keys():
                    options_to_add = action(players, active_player, self)
                    if options_to_add is not None: # This function has a playerchoice
                        added = True
                        card_options.append(options_to_add)
            if not added: # Nothing to be executed
                break
            options = {} # Dictionary for pretty user printing
            i = 1
            for option_list in card_options:
                for option in option_list:
                    options[i] = option
                    i+=1
            if len(options) == 1: # NO choice to be made
                chosen_option = 1
            else:
                chosen_option = players[active_player].strategy.chooseOption(options)
            # options[chosen_option] contains [function object, name of card, user text, integer related to choice]
            action = options[chosen_option][0]
            action(players, active_player, self, chosen_option=options[chosen_option][3])
            processed_cards[action] = True
