from Card import Card
from Option import Option

class LucMemento(Card):
    "Hit: You may spend 3 Time to gain a bonus to Power equal to your printed Power."

    def __init__(self):
        super().__init__(name="Memento", type=Card.Type.style, min_range=0, attack=0, priority=1, defense=0, hit=[self.bonusAttack])

    def __repr__(self):
        return super().__repr__()

    def bonusAttack(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        luc = players[active_player]
        if chosen_option is None:
            if luc.time_tokens >= 3:
                options = []
                options.append(Option(name=self.name, user_info="Do not spend Time Tokens.", params=0, function=self.bonusAttack))
                options.append(Option(name=self.name,
                user_info="Spend 3 Time Tokens to gain a bonus to Power equal to your printed Power.", params=1, function=self.bonusAttack))
                return options
            return None
        else:
            if chosen_option == 1:
                luc.time_tokens -= 3
                my_pair.attack += my_pair.base.attack
