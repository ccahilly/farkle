from gameConstants import NUM_DICE, POINT_SCORING_COMBINATIONS, VERBOSE, DEBUG
import random
from collections import Counter

class Player:
    def __init__(self, name):
        self.turn_score = 0
        self.dice_kept = 0
        self.name = name
    
    # Returns the score for the turn
    def take_turn(self):
        if VERBOSE:
            print(f"{self.name}'s turn")

        self.turn_score = 0
        self.dice_kept = 0

        roll = self.roll_dice()
        if VERBOSE:
            print(f"Initial roll: {roll}")

        while not self.farkle(roll):
            dice_to_keep = self.pick_dice_to_keep(roll)
            for dice in dice_to_keep:
                self.dice_kept += len(dice)
                self.turn_score += POINT_SCORING_COMBINATIONS[dice]
            
            if self.roll_again():
                roll = self.roll_dice()
                if VERBOSE:
                    print(f"Roll: {roll}")
            else:
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
    # Output type is a set of sorted tuples of tuples of integers.
    def possible_dice_to_keep(self, roll):
        if len(roll) == 0:
            return set()
        
        possibilities = set()
        for combo in POINT_SCORING_COMBINATIONS.keys():
            c = Counter(combo)
            if all(roll[k] >= c[k] for k in c):
                if DEBUG:
                    print(f"Roll: {roll}")
                    print(f"Combo: {combo}")
                    print(f"Remaining roll: {roll - c}")

                possibilities.add((combo,))
                sub_possibilities = self.possible_dice_to_keep(roll - c) # Set of sets of tuples

                for sub_combo in sub_possibilities:
                    possibilities.add(tuple(sorted((combo,) + sub_combo))) # sub_combo is a tuple of tuples

        return possibilities # Set of tuples of tuples
    
    # Output is true or false
    def farkle(self, roll):
        return len(self.possible_dice_to_keep(roll)) == 0