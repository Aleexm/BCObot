class Strategy:

    def __init__(self, strategy):
        self.strategy = strategy

    def __repr__(self):
        return "Strategy: {}".format(self.strategy.name)
