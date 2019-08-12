import sys
sys.path.append("..")
from Character import Character

class Shekhtur(Character):
    """Subclass of Character. Contains all Shekhtur-specific properties and methods, such as malice tokens and her possible antes."""
    malice_tokens = None
    def __init__(self, position, bases_hand, styles_hand, strategy, health):
        self.malice_tokens = 3
        super().__init__("Shekhtur", health=health, position=position, strategy=strategy, bases_hand=bases_hand, styles_hand=styles_hand)

    def __repr__(self):
        return super().__repr__(additional_params = "Malice: {}".format(self.malice_tokens))
