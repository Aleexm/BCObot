from Character import Character
from LucChrono import LucChrono
from LucFeinting import LucFeinting
from LucFusion import LucFusion
from LucMemento import LucMemento
from LucEternal import LucEternal
from LucTimeSurge import LucTimeSurge
from LucTimeRush import LucTimeRush
# from LucTimeStop import LucTimeStop
from Option import Option

class Luc(Character):
    """Subclass of Character. Contains all Luc-specific properties and methods, such as time tokens and his possible antes."""
    def __init__(self, position, bases_hand, styles_hand, strategy, health):
        self.time_tokens = 2
        super().__init__("Luc", health=health, position=position,
                         strategy=strategy, bases_hand=bases_hand,
                         styles_hand=styles_hand, end=[self.gainTime])

    def __repr__(self):
        return super().__repr__(additional_params = "Time: {}".format(self.time_tokens))

    def createCards():
        return LucChrono(), LucFeinting(), LucFusion(), LucMemento(), LucEternal()

    def gainTime(self, players, active_player, my_pair, opp_pair, chosen_option=None):
        """Either returns gaining 1 Time as an Option, or increments Time."""
        if chosen_option is None:
            return [Option(name=self.name, user_info="Gain 1 Time.", params=1, function=self.gainTime)]
        else:
            self.time_tokens = min(self.time_tokens+1, 5)

    def getPossibleAntes(self, used_antes):
        """Creates a list containing all possible antes for the current Luc.

        Parameters:
            used_antes (dict):Dictionary containing as keys the name of used antes this beat,
                              and as values True.
        Returns:
            possible_antes (list):List containing possible antes as Option.
            
        """
        possible_antes = super().getDefaultAntes(used_antes)
        time_surge = LucTimeSurge()
        time_rush = LucTimeRush()
        if time_surge.name in used_antes.keys() or time_rush.name in used_antes.keys():
            return possible_antes
        if self.time_tokens >= 1:
            possible_antes.append(Option(name=time_surge.name, user_info=time_surge.user_info, object=time_surge))
        if self.time_tokens >= 3:
            possible_antes.append(Option(name=time_rush.name, user_info=time_rush.user_info, object=time_rush))
        # if self.time_tokens == 5:
        #     time_stop = LucTimeStop()
        #     possible_antes.append(Option(name=time_stop.name, user_info=time_stop.user_info, object=time_stop))
        return possible_antes
