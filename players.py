from gameConstants import NUM_DICE
import random

class Player:
    def __init__(self):
        self.total_score = 0
        self.turn_score = 0
        self.dice_kept = 0
    
    def take_turn(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def roll_dice(self):
        roll = []
        
        # If all dice are kept, reset the kept dice count
        if self.dice_kept == NUM_DICE:
            self.dice_kept = 0

        for _ in range(NUM_DICE - self.dice_kept):
            roll.append(random.randint(1, 6))
        
        return roll.sort()
    
    def possible_dice_to_keep(self, roll):
        