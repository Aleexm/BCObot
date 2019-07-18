import numpy as np

class State:
    q_old = None
    q_new = None
    reward = None
    value = None
    terminal = None
    num_actions = None
    p1_health = None
    p2_health = None

    def __init__(self, terminal, num_actions, p1_health, p2_health, q_old = None, q_new = None, reward = 0, value = 0):
        self.terminal = terminal
        self.num_actions = num_actions
        self.p1_health = p1_health
        self.p2_health = p2_health
        self.q_old = np.repeat(0.0, num_actions) if q_old == None else q_old
        self.q_new = np.repeat(0.0, num_actions) if q_new == None else q_new
        if self.terminal: # Someone ded
            if p1_health > 0:
                self.reward = 1 # Won
            elif p2_health > 0:
                self.reward = -1 # Lost
            else:
                self.reward = 0 # Draw
        else:
            self.reward = 0
        self.value = value

    def __repr__(self):
        return "{}, {}, Q {}".format(self.p1_health, self.p2_health, self.q_old)
