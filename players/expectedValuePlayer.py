from .player import Player
from collections import Counter
from gameConstants import POINT_SCORING_COMBINATIONS, DEBUG
import numpy as np
from math import factorial

class ExpectedValuePlayer(Player):
    def __init__(self, name="ExpectedValuePlayer"):
        super().__init__(name=name)
        self.rolls_to_actions = {(): ()} # tuple to tuple of tuples
        self.fill_rolls_to_actions()
    
    def pick_dice_to_keep(self, roll):
        pass
    
    def roll_again(self):
        pass

    def fill_rolls_to_actions(self):
        if DEBUG:
            print("Filling rolls to actions")
            print(f"Rolls to actions: {self.rolls_to_actions}")
            print(f"Length of rolls to actions: {len(self.rolls_to_actions)}")
            
        expected_values_in_terms_of_r6 = np.array([[0,1], 
                                                   [np.nan, np.nan], 
                                                   [np.nan, np.nan], 
                                                   [np.nan, np.nan], 
                                                   [np.nan, np.nan], 
                                                   [np.nan, np.nan], 
                                                   [np.nan, np.nan]]) # [raw points, frac of r6]
        
        for num_dice in range(1,7):
            self.get_expected_value_rec(num_dice, expected_values_in_terms_of_r6)
            print(f"Expected value for {num_dice} dice in terms of r6: {expected_values_in_terms_of_r6[num_dice]}")

        if DEBUG:
            for roll, action in self.rolls_to_actions.items():
                points = 0
                for dice in action:
                    points += POINT_SCORING_COMBINATIONS[dice]
                print(f"Roll: {roll} Action: {action} Points: {points}")
                
    def get_expected_value_rec(self, num_dice, evs):
        if DEBUG:
            print(f"\nGetting expected value for {num_dice} dice")

        if not (np.isnan(evs[num_dice]).all()):
            return evs[num_dice]
        
        ev = np.zeros(2)
        new_rolls = dict()
        total_rolls = 0
        for roll in self.rolls_to_actions:
            if DEBUG:
                print(f"Roll from self.rolls_to_actions: {roll}")

            if len(roll) == num_dice - 1:
                for i in range(1, 7):
                    new_roll = tuple(sorted(roll + (i,)))
                    if new_roll in new_rolls:
                        continue
                    
                    total_rolls += unique_orderings(new_roll)
                    
                    possible_plays = list(self.possible_dice_to_keep(Counter(new_roll)))
                    play_values = np.zeros((len(possible_plays), 2))
                    
                    for i, play in enumerate(possible_plays):
                        updated_num_dice = num_dice
                        for combo in play:
                            play_values[i][0] += POINT_SCORING_COMBINATIONS[combo] * unique_orderings(new_roll)
                            updated_num_dice -= len(combo)

                        play_values[i] += self.get_expected_value_rec(updated_num_dice, evs) * unique_orderings(new_roll)

                    if len(possible_plays) == 0:
                        new_rolls[new_roll] = () # No move in the case of a farkle
                    else:
                        max_raw_points = np.argmax(play_values, axis=0)[0]
                        max_r_indices = np.where(play_values[:, 1] == np.max(play_values[:, 1]))[0]
                        if max_raw_points in max_r_indices:
                            ev += play_values[max_raw_points]
                            new_rolls[new_roll] = possible_plays[max_raw_points]
                        else:
                            # raise ValueError(f"Best play not clear without knowing the value of r6: {new_roll} {play_values} {possible_plays}")
                            print("Best play not clear without knowing the value of r6")
                            print(f"Roll: {new_roll}")
                            print(f"Play values: {play_values}")
                            print(f"Possible plays: {possible_plays}")
                            ev += play_values[max_raw_points]
                            new_rolls[new_roll] = possible_plays[max_raw_points]

        if DEBUG:
            print(f"Expected value counts: {ev}")
        
        if total_rolls != 6 ** num_dice:
            raise ValueError(f"Expected value calculation error: {total_rolls} {6 ** num_dice}")

        evs[num_dice] = ev / 6 ** num_dice
        self.rolls_to_actions.update(new_rolls)

def unique_orderings(lst):
    # Count frequencies of each element
    freq = Counter(lst)
    
    # Compute the numerator (n!)
    n_fact = factorial(len(lst))
    
    # Compute the denominator (product of k_i!)
    denom = 1
    for count in freq.values():
        denom *= factorial(count)
    
    # Compute the number of unique orderings
    return n_fact // denom