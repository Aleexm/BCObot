from Card import Card

class LucMemento(Card):
    "Contains all functionality for Luc's Memento style."

    def __init__(self):
        super().__init__(name="Memento", type=Card.Type.style, min_range=0, attack=0, priority=1, defense=0, hit=[self.bonusAttack])

    def __repr__(self):
        return super().__repr__()

    def bonusAttack(self, players, active_player, my_pair, chosen_option=None):
        """
        Hit: You may spend 2 Time Tokens to gain a bonus to Power equal
        "to your printed Power.
        """
        luc = players[active_player]
        if chosen_option is None:
            if luc.time_tokens >= 2:
                options = []
                options.append([self.bonusAttack, "({})".format(self.name), "Do not spend Time Tokens.", 0])
                options.append([self.bonusAttack, "({})".format(self.name), "Spend 2 Time Tokens to gain a bonus to Power equal to your printed Power.", 1])
                return options
            return None
        else:
            if chosen_option == 1:
                my_pair.attack += my_pair.base.attack
