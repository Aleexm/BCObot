import numpy as np
from Option import Option

class Beat:

    def __init__(self, played_pairs):
            self.played_pairs = played_pairs

    def ante(self, players, first_player):
        passed = [False, False]
        active_player_idx = first_player
        active_player = players[first_player]
        used_antes = [{}, {}]
        while not all(passed):
            if not passed[active_player_idx]:
                possible_antes = active_player.getPossibleAntes(used_antes[active_player_idx])
                options = {}
                options[1] = Option(name="Pass", user_info="Pass.", params=0)
                for i,ante_option in enumerate(possible_antes):
                    options[i+2] = ante_option
                if len(options) == 1:
                    chosen_option = 1
                else:
                    chosen_option = active_player.strategy.chooseOption(options)
                if chosen_option == 1: # "Pass"
                    print("{} Pass".format(active_player_idx))
                    passed[active_player_idx] = True
                    continue
                chosen_ante = options[chosen_option]
                print("{} {}".format(active_player_idx, chosen_ante.user_info))
                chosen_ante.object.apply(self, players, active_player_idx)
                used_antes[active_player_idx][chosen_ante.object.name] = True
            active_player_idx = 1-active_player_idx
            active_player = players[active_player_idx]


    def executeActions(self, action_name, players, active_player):
        processed_cards = {} # dict containing cards whose actions we've executed
        while True:
            added = False # Boolean to check whether any actions remain
            card_options = []
            for action in action_name: # action is a function object, i.e. chrono.close
                if action not in processed_cards.keys():
                    options_to_add = action(players, active_player, self.played_pairs[active_player], self.played_pairs[1-active_player])
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
            action = options[chosen_option].function
            print(options[chosen_option].user_info)
            action(players, active_player, self.played_pairs[active_player], self.played_pairs[1-active_player], chosen_option=options[chosen_option].params)
            processed_cards[action] = True

    def execute(self, players):
        stunned = [False, False] # If Stun Guard is broken, set to True
        # Get the index of the first player (0 or 1)
        print(self.played_pairs)
        if self.played_pairs[0].priority == self.played_pairs[1].priority:
            return
        first_player = np.argmax([self.played_pairs[0].priority, self.played_pairs[1].priority])
        print(first_player)
        self.ante(players, first_player)
        print("{} Start".format(first_player))
        self.executeActions(self.played_pairs[first_player].start, players, active_player=first_player) # START actions
        self.executeActions(players[first_player].start, players, active_player=first_player)
        print("{} Start".format(1-first_player))
        self.executeActions(self.played_pairs[1-first_player].start, players, active_player=1-first_player)
        self.executeActions(players[1-first_player].start, players, active_player=1-first_player)
        for i in range(2): # Both players get to attack once
            p1_idx = (first_player + i) % 2 # Initially just firstplayer
            p1 = players[p1_idx]
            p2_idx = (first_player + i + 1) % 2 # Afterwards, other player
            p2 = players[p2_idx]
            attacking_pair = self.played_pairs[p1_idx]# Get card of attacker
            defending_pair = self.played_pairs[p2_idx]
            if not stunned[p1_idx] and p1.health > 0:
                print("{} Before".format(p1_idx))
                self.executeActions(attacking_pair.before, players, active_player=p1_idx) # BEFORE actions
                self.executeActions(players[p1_idx].before, players, active_player=p1_idx)
                position_difference = abs(np.diff([p1.position, p2.position]))
                if position_difference >= attacking_pair.min_range and position_difference <= attacking_pair.max_range:
                    print("{} Hit".format(p1_idx))
                    self.executeActions(players[p1_idx].hit, players, active_player=p1_idx)
                    self.executeActions(attacking_pair.hit, players, active_player=p1_idx)
                    print("{} On_Hit".format(p2_idx))
                    self.executeActions(defending_pair.on_hit, players, active_player=p2_idx)
                    self.executeActions(players[p2_idx].on_hit, players, active_player=p2_idx)
                    damage = max(attacking_pair.attack - defending_pair.soak, 0)
                    print("Damage to {}: {}".format(p2_idx, damage))
                    p2.health = max(0, p2.health - damage) # Clamp hp at 0
                    if damage > 0 and (defending_pair.defense < damage or p1.StaticEffects.ignore_stun_guard in p1.static_effects):
                        stunned[p2_idx] = True # Stun Guard broken
                print("{} After".format(p1_idx))
                self.executeActions(attacking_pair.after, players, active_player=p1_idx) # AFTER actions
                self.executeActions(players[p1_idx].after, players, active_player=p1_idx)

        print("{} End".format(first_player))
        self.executeActions(self.played_pairs[first_player].end, players, active_player=first_player)
        print("{} End".format(1-first_player))
        self.executeActions(self.played_pairs[1-first_player].end, players, active_player=1-first_player)
        print("Closing")
        self.executeActions(players[first_player].end, players, active_player=first_player)
        self.executeActions(players[1-first_player].end, players, active_player=1-first_player)
        for player in players:
            print(player)
