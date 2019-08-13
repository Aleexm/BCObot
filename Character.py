from strategies.Strategy import Strategy
from copy import deepcopy
from Option import Option
from Pair import Pair
from collections import deque
from default_antes.AnteGuardUp import AnteGuardUp
from default_antes.AntePowerUp import AntePowerUp
from default_antes.AntePriorityUp import AntePriorityUp
from enum import Enum

class Character:
    """Contains all properties a Fighter in BCO has, such as his health, position, as well as Character-based functionality, such as moving and playing a Pair."""
    def __init__(self, name, health, position, strategy, bases_hand=None, styles_hand=None, pairs_discard=None, force=2, start=[], before=[], hit=[], on_hit=[], after=[], end=[]):
        self.name = name
        self.health = health
        self.position = position
        self.bases_hand = list(bases_hand)
        self.styles_hand = list(styles_hand)
        self.pairs_discard = deque([]) if pairs_discard is None else deque(pairs_discard)
        self.strategy = strategy
        self.force = force
        self.start = start
        self.before = before
        self.hit = hit
        self.on_hit = on_hit
        self.after = after
        self.end = [self.gainForce] + end
        self.static_effects = {}

    def __repr__(self, additional_params):
        return "Character: {}, Health: {}, Position: {}, Force: {}, discard: {}, {}".format(
        self.name, self.health, self.position, self.force, self.pairs_discard, additional_params)

    class StaticEffects(Enum):
        cant_be_moved = 1
        cant_move = 2
        ignore_stun_guard = 3
        stun_immunity = 4

    def getPossibleMoves(self, moves_list, players, active_player):
        """ Returns a list of all moves for a character, based on his possible moves.

        Parameters:
            moves_list (list):The list of possible moves, i.e. [1,2] for Advance 1 or 2.
            players (list): list containing [player1, player2].
            active_player (int): 0 or 1, resembling which entry in players is moving.
        Returns:
            possible_moves(list):The list of possible moves for this character.

        """
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
        """ Moves the active player to_move squares.

        Parameters:
            to_move (int): The number of steps to move. (initially) Positive for advance, negative for retreat.
            players (list): list containing [player1, player2].
            active_player (int): 0 or 1, resembling which entry in players is moving.

        """
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
            # Out of bounds:  This should never happen, out of bounds should be caught outside of this method
            print("can't move...")
        else: # We can move!
            new_position = p1.position + to_move
            p1.position = new_position

    def getDefaultAntes(self, used_antes):
        """ Returns the three basic antes as Options, given that they have not yet been anted.

        Parameters:
            used_antes (dict):Dictionary containing as keys the names of used antes and as values True.

        Returns:
            options (list):List containing all possible basic antes.

        """
        options = []
        if self.force < 2: # Can't ante anything
            return options
        else:
            power, prio, guard = AntePowerUp(), AntePriorityUp(), AnteGuardUp()
            default_antes = [power, prio, guard]
            for ante in default_antes:
                if ante.name not in used_antes.keys(): # We have not yet anted this ante.
                    options.append(Option(name=ante.name, user_info=ante.user_info, object=ante))
            return options

    def gainForce(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        """ Increments players' force at the end of turn.

        Parameters:
            players (list):list containing [player1, player2].
            active_player (int):0 or 1, resembling which entry in players is gaining Force.
            my_pair (Pair):active_player's played Pair.
            opp_pair (Pair):other player's played Pair.
            chosen_option (int):Integer reflecting the updated force of this character.

        """
        if chosen_option is None:
            return [Option(name=self.name, user_info="Gain Force.", params= min(self.force + (2-int((self.health-1)/10)), 10), function=self.gainForce)]
        else:
            self.force = chosen_option

    def choosePair(self, bases_hand, styles_hand, action_name="play"):
        """ Choose a Pair consisting of a Base and Style from all cards in hand.

        Parameters:
            action_name (str):String containing user information to be shown if applicable in its strategy.

        Returns:
            Pair (Pair):The chosen Pair consisting of a Base and Style.
            bases_hand (list of Card):Bases in hand (not the same as self.bases, as clashes happen).
            styles_hand (list of Card):Styles in hand.

        """
        base_options = {}
        for i,base in enumerate(bases_hand):
            base_options[i+1] = Option(name=action_name, user_info = base.name, params=i)
        style_options = {}
        for i,style in enumerate(styles_hand):
            style_options[i+1] = Option(name=action_name, user_info = style.name, params=i)
        chosen_option = self.strategy.chooseOption(base_options, header="Choose a base to {}".format(action_name))
        chosen_base = base_options[chosen_option].params
        chosen_option = self.strategy.chooseOption(style_options, header="Choose a style to {}".format(action_name))
        chosen_style = style_options[chosen_option].params
        return Pair(bases_hand[chosen_base], styles_hand[chosen_style])

    def playPair(self, pair_to_play):
        """ Enqueues the Pair in the pairs_discard queue,
        and adds the first Pair in line in pairs_discard to hand.

        Parameters:
            pair_to_play (Pair):The pair that will be played.
        """
        played_pair = self.choosePair(bases_hand=self.bases_hand, styles_hand=self.styles_hand)
        pair_to_hand = self.pairs_discard.popleft()
        self.bases_hand.append(pair_to_hand.base)
        self.styles_hand.append(pair_to_hand.style)
        self.bases_hand.remove(played_pair.base)
        self.styles_hand.remove(played_pair.style)
        self.pairs_discard.append(played_pair)

    def initHand(self):
        """Discards two Pairs from your hand and adds them to your discard queue."""
        for discards in range(2):
            chosen_pair = self.choosePair(bases_hand=self.bases_hand, styles_hand=self.styles_hand, action_name="discard")
            self.pairs_discard.append(chosen_pair)
            self.bases_hand.remove(chosen_pair.base)
            self.styles_hand.remove(chosen_pair.style)

    def testInitHand(self, x):
        """Discards two Pairs from your hand and adds them to your discard queue."""
        bases_hand_1 = [self.bases_hand[0-x]]
        styles_hand_1 = [self.styles_hand[0-x]]
        bases_hand_2 = [self.bases_hand[1-x]]
        styles_hand_2 = [self.styles_hand[1-x]]
        for discards in range(2):
            if discards == 0:
                chosen_pair = self.choosePair(bases_hand=bases_hand_1, styles_hand=styles_hand_1, action_name="discard")
            else:
                chosen_pair = self.choosePair(bases_hand=bases_hand_2, styles_hand=styles_hand_2, action_name="discard")
            self.pairs_discard.append(chosen_pair)
            self.bases_hand.remove(chosen_pair.base)
            self.styles_hand.remove(chosen_pair.style)
