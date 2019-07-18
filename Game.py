from State import State
from Card import Card
from Character import Character
from Luc import Luc
from Shekhtur import Shekhtur
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.pyplot import figure

def winner(p1, p2):
    '''
    Checks whether the game has terminated, and returns the correspondin player if it did.
    Returns False if no winner yet, None if draw (probably change this later as it's kinda weird)
    Arguments:
        p1: Character 1, you
        p2: Character 2, opponent
    '''
    if p1.health <= 0 and p2.health > 0:
        return p2
    elif p2.health <= 0 and p1.health > 0:
        return p1
    elif p1.health <= 0 and p2.health <= 0:
        return None
    else:
        return False

def plotValues(states):
    '''
    Plots, for each of the 21x21 states, the corresponding value and the best action.
    '''
    size_x = np.shape(states)[0]
    size_y = np.shape(states)[1]
    figure(num=None, figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    vals = np.arange(float(size_x * size_y)).reshape(size_x, size_y)
    for i in range(size_x):
        for j in range(size_y):
            vals[i][j] = np.amax(states[i][j].q_old)
    cmap = plt.get_cmap()
    cmap.set_bad('black')
    masked_vals = np.ma.masked_equal(vals, 0.0)
    im = plt.imshow(masked_vals, interpolation = 'nearest', cmap=cmap)
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im)
    ticks = range(21)
    plt.xticks(ticks, ticks[::-1])
    plt.yticks(ticks, ticks[::-1])
    plt.xlabel("Opp Health", size=14)
    plt.ylabel("My Health", size=14)
    for i in range(size_x):
        for j in range(size_y):
            if vals[i][j] == 0.0:
                continue # We haven't explored all actions in this state
            plt.annotate(np.argmax(states[i][j]), (j,i), color = 'white')

    plt.title("Best action and its value, from your perspective")
    # plt.tight_layout()
    fig = plt.gcf()
    # fig.savefig('gamma{}.jpg'.format(gamma), bbox_inches='tight')
    plt.show()

def evalRound(players, played_cards, states):
    '''
    Evaluates you and your opponent's cards played and updates health. Returns
    the corresponding new state after this round
    Arguments:
        players: List of players: [you, opponent]
        played_cards: List of played cards: [your_card, opp_card]
        states: Q-table containing all Q-values for each of the 21x21 states
    '''
    stunned = [False, False] # If Stun Guard is broken, set to True
    # Get the index of the first player (0 or 1)
    first_player = np.argmax([played_cards[0].priority, played_cards[1].priority]) \
                   if played_cards[0].priority != played_cards[1].priority \
                   else print("Clash") # TODO: Clash functionality

    for i in range(2): # Both players get to attack once
        attacking_player_idx = (first_player + i) % 2 # Initially just firstplayer
        defending_player_idx = (first_player + i + 1) % 2 # Afterwards, other player
        current_card = played_cards[attacking_player_idx] # Get card of attacker
        if not stunned[attacking_player_idx]:
            if abs(players[attacking_player_idx].position - players[defending_player_idx].position) <= current_card.range: # Hit
                players[defending_player_idx].health = max(0, players[defending_player_idx].health - current_card.attack) # Clamp hp at 0
                if played_cards[defending_player_idx].defense < current_card.attack:
                    stunned[defending_player_idx] = True # Stun Guard broken

    # TODO: If both died, know who won
    # states[0][0] represents both players at 20hp, so it's inverted.
    return states[len(states) -1- players[0].health][len(states) -1- players[1].health]

def initStates(num_actions, max_health):
    '''
    Initializes the Q-value states, where all actions are initialized to 0.
    Returns the corresponding states array
    Arguments:
        num_actions: number of cards one can play
        max_health: The maximum health of both characters (usually just 20).
    '''
    states = [[] for i in range(health+1)] # 21x21 array of class State
    for i in range(max_health+1): # We need a state for health = 0...20, so 21 in total.
        for j in range(max_health+1):
            if j == max_health or i == max_health:
                # states[0][0] = 20vs20 hp. states[max_healh][max_health] therefore is 0vs0 hp: Terminal!
                states[i].append(State(True, num_actions, max_health-i, max_health-j))
            else:
                states[i].append(State(False, num_actions, max_health-i, max_health-j))
    return states


def QLearning(passed_states, passed_players, gamma, alpha, epsilon, episodes):
    '''
    The learning part! Updates the Q-value states array with learned values for
    each possible action (number of cards that can be played), for each of the 21x21 states.
    See https://en.wikipedia.org/wiki/Q-learning
    Arguments:
        passed_states: Q-value states array
        passed_players: list of players: [me, opp]
        my_actions: list of cards I can play
        opp_actions: list of cards my opponent can play
        gamma: discount factor, higher/lower gamma means we care more/less about distant rewards
        alpha: Learning rate: trade-off parameter between current state-action estimate and newly observed value.
                              Higher/Lower alpha = more/less weight to newly observed value
        epsilon: Take a random action with probability 0<=epsilon<=1 (exploration/exploitation tradeoff)
        episodes: Number of games you want to simulate.
    '''
    states = copy.deepcopy(passed_states)
    my_actions = passed_players[0].cards
    opp_actions = passed_players[1].cards
    # diffs = np.zeros(episodes) + float("Infinity")
    for episode in range(episodes): # Repeat for number of games to be simulated
        if episode%10000 == 0:
            print(episode)
        players = copy.deepcopy(passed_players) # Reset all health, position etc to passed values
        current_state = states[0][0] # Start both players at full health (recall states[0][0] is 20vs20 HP)
        while not current_state.terminal:
            my_action = np.argmax(current_state.q_old)
            if random.random() < epsilon:
                my_action = random.randint(0, len(my_actions)-1)
            opp_action = random.randint(0, len(opp_actions)-1)
            new_state = evalRound(players, [my_actions[my_action], opp_actions[opp_action]], states)
            current_state.q_old[my_action] = current_state.q_old[my_action] \
                                             + alpha * (new_state.reward + gamma * np.amax(new_state.q_old) - current_state.q_old[my_action])
            current_state = new_state

        # extractMax(states)
        # diffs[episode] = getDiff(states)
    return states

# Test stuff
card_attack = Card("Attack", range=1, attack=2, priority=3, defense=0)
card_defense = Card("Defense", range=1, attack=1, priority=0, defense=5)
card_priority = Card("Priority", range=1, attack=1, priority=4, defense=0)
card_trash = Card("Trash", range=1, attack=2, priority=1, defense=0)

my_actions = [card_attack, card_defense]
opp_actions = [card_priority, card_trash]
health = 20
luc = Luc(position=0, cards=my_actions, health=health)
shekhtur = Shekhtur(position=1, cards=opp_actions, health=health)
states = initStates(num_actions=2, max_health=health)

players = [luc, shekhtur]
states = QLearning(states, players, gamma=0.9, alpha=0.1, epsilon=0.05, episodes=1000000)
for state_row in states:
    for state in state_row:
        print(state)
plotValues(states)
