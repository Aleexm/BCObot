import sys
sys.path.append("..")
import numpy as np
from Option import Option
from copy import deepcopy
from Pair import Pair

class Beat:
    """Beat instances are generated per beat, and contain the played pairs as well as generic beat functionality, such as executing cards' actions."""
    def __init__(self, played_pairs, round):
            self.played_pairs = played_pairs
            self.round = round

    def ante(self, players, first_player):
        """Gets the both players' antes of this beat.

        Parameters:
            players (list): list containing [player1, player2].
            first_player (int): 0 or 1, resembling which entry in players is ante'ing first.

        Returns:
            antes_to_apply (list of Antes): antes_to_apply[0][1] contains player 0's second ante to apply.
        """
        passed = [False, False] # Set to True if that player has passed.
        active_player_idx = first_player
        active_player = players[first_player]
        used_antes = [{}, {}] # used_antes[0]['Priority Up'] = True if player 0 ante'd Priority Up.
        antes_to_apply = [[], []]
        while not all(passed): # A player still wants to ante
            possible_antes = active_player.getPossibleAntes(used_antes[active_player_idx])
            options = {} # Dictionary to contain as keys integers [1, 2, ...] and as values the ante Options.
            options[1] = Option(name="Pass", user_info="Pass.", params=0)
            for i,ante_option in enumerate(possible_antes):
                options[i+2] = ante_option
            if len(options) == 1: # No choice to be made.
                chosen_option = 1
            else:
                chosen_option = active_player.strategy.chooseOption(options)
            if chosen_option == 1: # "Pass"
                print("{} Pass".format(active_player_idx))
                passed[active_player_idx] = True
            else:
                passed[1-active_player_idx] = False
                chosen_ante = options[chosen_option]
                print("{} {} {}".format(active_player_idx, chosen_ante.name, chosen_ante.user_info))
                antes_to_apply[active_player_idx].append(chosen_ante.object)
                chosen_ante.object.payCost(self, players, active_player_idx) # Applies the ante's effect.
                used_antes[active_player_idx][chosen_ante.object.name] = True
            active_player_idx = 1-active_player_idx # Other player to ante now.
            active_player = players[active_player_idx]
        return antes_to_apply


    def executeActions(self, action_name, players, active_player):
        """ Executes fighter's and card's phase-actions, i.e. Start: ..., End: ... etc.
        Parameters:
            action_name (list):List containing all functions for a phase. Property of Card or Character class. (Card.start, Card.end)
            players (list): list containing [player1, player2].
            active_player (int): 0 or 1, resembling which entry in players is executing actions.

        """
        processed_actions = {} # dict containing actions we've executed as keys, and True as vals
        while True:
            added = False # Boolean to check whether any actions remain
            action_options = []
            for action in action_name: # action is a function object, i.e. chrono.close
                if action not in processed_actions.keys():
                    options_to_add = action(players, active_player, self.played_pairs[active_player], self.played_pairs[1-active_player])
                    if options_to_add is not None: # This function has a playerchoice
                        added = True
                        action_options.append(options_to_add)
            if not added: # Nothing to be executed
                break
            options = {} # Dictionary for pretty user printing
            i = 1
            for option_list in action_options:
                for option in option_list:
                    options[i] = option
                    i+=1
            if len(options) == 1: # No choice to be made
                chosen_option = 1
            else:
                chosen_option = players[active_player].strategy.chooseOption(options)
            action = options[chosen_option].function
            print(options[chosen_option].name, options[chosen_option].user_info)
            action(players, active_player, self.played_pairs[active_player], self.played_pairs[1-active_player], chosen_option=options[chosen_option].params)
            processed_actions[action] = True

    def applyAntesToPairs(self, players, antes_to_apply):
        """Applies the antes_to_apply to the played pairs."""
        for player_idx in [0, 1]:
            if len(antes_to_apply[player_idx]) > 0:
                for ante in antes_to_apply[player_idx]:
                    ante.apply(self, players, player_idx)

    def handleClashes(self, players, antes_to_apply):
        p0_bases_hand = deepcopy(players[0].bases_hand)
        p1_bases_hand = deepcopy(players[1].bases_hand)
        self.applyAntesToPairs(players, antes_to_apply)
        while self.played_pairs[0].priority == self.played_pairs[1].priority and len(p0_bases_hand) > 1 and len(p1_bases_hand) > 1:
            print("Clashed pair: {}.".format(self.played_pairs))
            p0_bases_hand = [card for card in p0_bases_hand if card.name != self.played_pairs[0].base.name]
            p1_bases_hand = [card for card in p1_bases_hand if card.name != self.played_pairs[1].base.name]
            new_p0_base = players[0].chooseBase(action_name="play", bases_hand=p0_bases_hand)
            new_p1_base = players[1].chooseBase(action_name="play", bases_hand=p1_bases_hand)
            self.played_pairs = [Pair(new_p0_base, self.played_pairs[0].style), Pair(new_p1_base, self.played_pairs[1].style)]
            self.applyAntesToPairs(players, antes_to_apply)

    def execute(self, players):
        """Executes a Beat, givenplayers (list): list containing [player1, player2]."""
        antes_to_apply = self.ante(players, 1)
        self.handleClashes(players, antes_to_apply)
        players[0].playPair(self.played_pairs[0])
        players[1].playPair(self.played_pairs[1])
        stunned = [False, False] # If Stun Guard is broken, set to True
        print(self.played_pairs)
        first_player = np.argmax([self.played_pairs[0].priority, self.played_pairs[1].priority])
        print(first_player)
        print("{} Start".format(first_player))
        self.executeActions(self.played_pairs[first_player].start, players, active_player=first_player) # START card actions
        self.executeActions(players[first_player].start, players, active_player=first_player) # START character actions
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
                self.executeActions(attacking_pair.before, players, active_player=p1_idx)
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
