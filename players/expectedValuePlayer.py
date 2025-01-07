from .player import Player
from collections import Counter
from gameConstants import POINT_SCORING_COMBINATIONS, DEBUG
import numpy as np

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
        
        for num_dice in range(1, 7):
            self.get_expected_value_rec(num_dice, expected_values_in_terms_of_r6)
            print(f"Expected value for {num_dice} dice in terms of r6: {expected_values_in_terms_of_r6[num_dice]}")

    def get_expected_value_rec(self, num_dice, evs):
        if DEBUG:
            print(f"Getting expected value for {num_dice} dice")

        if evs[num_dice] is not [np.nan, np.nan]:
            return evs[num_dice]
        
        ev = np.zeros(2)
        for roll in self.rolls_to_actions:
            if DEBUG:
                print(f"Roll: {roll}")

            if len(roll) == num_dice - 1:
                for i in range(1, 7):
                    new_roll = roll + (i,)
                    new_roll.sort()

                    possible_plays = self.possible_dice_to_keep(Counter(new_roll))
                    play_values = np.zeros((len(possible_plays), 2))
                    
                    for i, play in enumerate(possible_plays):
                        updated_num_dice = num_dice
                        for combo in play:
                            play_values[i][0] += POINT_SCORING_COMBINATIONS[combo]
                            updated_num_dice -= len(combo)

                        play_values[i] += self.get_expected_value_rec(updated_num_dice, evs)

                    # Ignore in the case of a farkle
                    if len(possible_plays) > 0:
                        max_indices = np.argmax(play_values, axis=0)
                        if max_indices[0] == max_indices[1]:
                            ev += play_values[max_indices[0]]
                        else:
                            raise ValueError(f"Best play not clear without knowing the value of r6: {new_roll}")
        evs[num_dice] = ev / 6 ** num_dice