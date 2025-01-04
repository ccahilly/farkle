from gameConstants import NUM_DICE, POINT_SCORING_COMBINATIONS
import random

class Player:
    def __init__(self):
        self.total_score = 0
        self.turn_score = 0
        self.dice_kept = 0
    
    def take_turn(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def roll_dice(self):
        roll = {}
        
        # If all dice are kept, reset the kept dice count
        if self.dice_kept == NUM_DICE:
            self.dice_kept = 0

        for _ in range(NUM_DICE - self.dice_kept):
            roll.add(random.randint(1, 6))
        
        return roll
    
    # Roll is a set of integers representing the dice roll.
    # Returns the set of all possible dice to keep.
    # Output type is a set of sets of tuples of integers.
    def possible_dice_to_keep(self, roll):
        if len(roll) == 0:
            return {}
        
        possibilities = {}
        for combo in POINT_SCORING_COMBINATIONS.keys():
            if set(combo) in roll:
                sub_possibilities = self.possible_dice_to_keep_rec(roll - set(combo)) # Set of sets of tuples

                if len(sub_possibilities) == 0:
                    possibilities.add({combo})
                else:
                    for sub_combo in sub_possibilities.keys():
                        possibilities.add({combo} + sub_combo) # sub_combo is a set of tuples

        return possibilities # Set of sets of tuples
        
    def pick_dice_to_keep(self, roll):
        raise NotImplementedError("Subclasses must implement this method")