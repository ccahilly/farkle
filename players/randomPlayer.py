from .player import Player
import random

class RandomPlayer(Player):
    def __init__(self):
        super().__init__(name="Random")
    
    def pick_dice_to_keep(self, roll):
        possibilities = self.possible_dice_to_keep(roll)
        return random.choice(list(possibilities))
    
    def roll_again(self):
        return random.choice([True, False])