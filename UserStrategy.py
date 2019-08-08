from Strategy import Strategy
import random

class UserStrategy(Strategy):

    def __init__(self):
        self.name = "User"
        super().__init__(self)

    def __repr__(self):
        return super().__repr__()

    def chooseOption(self, options):
        chosen = False
        chosen_option = None
        for key,val in options.items():
            print("{}: {}: {}".format(key, val[1], val[2]))
        while(not chosen):
            inp = input("Choose your move: ")
            try:
                chosen_option = int(inp)
            except ValueError:
                pass
            if chosen_option not in options.keys():
                print("Invalid option.")
            else:
                chosen=True
        return chosen_option
