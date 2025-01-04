from gameConstants import NUM_DICE, POINT_SCORING_COMBINATIONS
import random

class Player:
    def __init__(self):
        self.total_score = 0
        self.turn_score = 0
        self.dice_kept = 0
    
    def take_turn(self):
        roll = self.roll_dice()
        self.turn_score = 0

        while not self.farkle(roll):
            dice_to_keep = self.pick_dice_to_keep(roll)
            for dice in dice_to_keep:
                self.dice_kept -= len(dice)
                self.turn_score += POINT_SCORING_COMBINATIONS[dice]
            
            if self.roll_again(roll):
                roll = self.roll_dice()
            else:
                break

    def roll_dice(self):
        roll = {}
        
        # If all dice are kept, reset the kept dice count
        if self.dice_kept == NUM_DICE:
            self.dice_kept = 0

        for _ in range(NUM_DICE - self.dice_kept):
            roll.add(random.randint(1, 6))
        
        return roll
    
    # Output type is a set of tuples of integers and the associated points
    def pick_dice_to_keep(self, roll):
        raise NotImplementedError("Subclasses must implement this method")
    
    # Output is true or false
    def roll_again(self, roll):
        raise NotImplementedError("Subclasses must implement this method")

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
    
    def farkle(self, roll):
        return len(self.possible_dice_to_keep(roll)) == 0