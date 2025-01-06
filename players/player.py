from gameConstants import NUM_DICE, POINT_SCORING_COMBINATIONS, VERBOSE, DEBUG
import random
from collections import Counter

class Player:
    def __init__(self, name):
        self.total_score = 0
        self.turn_score = 0
        self.dice_kept = 0
        self.name = name
    
    # Returns the score for the turn
    def take_turn(self):
        if VERBOSE:
            print(f"{self.name}'s turn")

        self.turn_score = 0
        roll = self.roll_dice()
        if DEBUG:
            print(f"Initial roll: {roll}")

        while not self.farkle(roll):
            if VERBOSE:
                print(f"Roll: {roll}")
            
            dice_to_keep = self.pick_dice_to_keep(roll)
            for dice in dice_to_keep:
                self.dice_kept += len(dice)
                self.turn_score += POINT_SCORING_COMBINATIONS[dice]
            
            if self.roll_again():
                roll = self.roll_dice()
            else:
                self.total_score += self.turn_score
                return self.turn_score

        # If the player farkles, the turn score is 0.
        # Add nothing to the total score.
        return 0

    # Output type is a Counter of integers (keys 1-6)
    def roll_dice(self):
        roll = Counter()
        
        # If all dice are kept, reset the kept dice count
        if self.dice_kept == NUM_DICE:
            self.dice_kept = 0

        for _ in range(NUM_DICE - self.dice_kept):
            roll[random.randint(1, 6)] += 1

        return roll
    
    # Output type is a set of tuples of integers and the associated points
    def pick_dice_to_keep(self, roll):
        raise NotImplementedError("Subclasses must implement this method")
    
    # Output is true or false
    def roll_again(self):
        raise NotImplementedError("Subclasses must implement this method")

    # Roll is a Counter of integers representing the dice roll.
    # Returns the set of all possible dice to keep.
    # Output type is a set of lists of tuples of integers.
    def possible_dice_to_keep(self, roll):
        if len(roll) == 0:
            return set()
        
        possibilities = set()
        for combo in POINT_SCORING_COMBINATIONS.keys():
            remaining_roll = roll - Counter(combo)
            if not any(v < 0 for v in remaining_roll.values()):
                sub_possibilities = self.possible_dice_to_keep(remaining_roll) # Set of sets of tuples

                if len(sub_possibilities) == 0:
                    possibilities.add({combo})
                else:
                    for sub_combo in sub_possibilities.keys():
                        possibilities.add({combo} + sub_combo) # sub_combo is a set of tuples

        return possibilities # Set of sets of tuples
    
    # Output is true or false
    def farkle(self, roll):
        return len(self.possible_dice_to_keep(roll)) == 0