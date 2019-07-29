import numpy as np

class State:
    q_old = None
    reward = None
    terminal = None
    num_actions = None
    p1_health = None
    p2_health = None

    def __init__(self, terminal, num_actions, p1_health, p2_health, q_old = None, reward = 0):
        self.terminal = terminal
        self.num_actions = num_actions
        self.p1_health = p1_health
        self.p2_health = p2_health
        self.q_old = np.repeat(0.0, num_actions) if q_old == None else q_old
        if self.terminal: # Someone ded
            if p1_health > 0:
                self.reward = 1 # Won
            elif p2_health > 0:
                self.reward = -1 # Lost
            else:
                self.reward = 0 # Draw TODO: No draw possible
        else:
            self.reward = 0

    def __repr__(self):
        return "{}, {}, Q {}".format(self.p1_health, self.p2_health, self.q_old)
