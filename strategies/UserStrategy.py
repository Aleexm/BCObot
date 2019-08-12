import sys
sys.path.append("..")
from .Strategy import Strategy

class UserStrategy(Strategy):
    """Lets the user decide between all presented Options."""
    def __init__(self):
        self.name = "User"
        super().__init__(self)

    def __repr__(self):
        return super().__repr__()

    def chooseOption(self, options, header=None):
        """Choose an option.

        Parameters:
            options (dict):Dictionary containing as keys ints [1,2,...] and as values
                           Option objects.
            header (str):Options header, such as "Please choose a Pair to discard."

        Returns:
            chosen_option (int):The dictionary key index which we have chosen.

        """
        chosen = False
        chosen_option = None
        if header is not None:
            print(header)
        for key,val in options.items():
            print("{}: {}: {}".format(key, val.name, val.user_info))
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
