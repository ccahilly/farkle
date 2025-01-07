from .player import Player
from collections import Counter
from gameConstants import POINT_SCORING_COMBINATIONS
import numpy as np

class ExpectedValuePlayer(Player):
    def __init__(self, name="ExpectedValuePlayer"):
        super().__init__(name=name)
        self.possible_rolls = {(): ()} # tuple to tuple of tuples
    
    def pick_dice_to_keep(self, roll):
        pass
    
    def roll_again(self):
        pass

    def get_expected_value_in_terms_of_r6(self):
        expected_values = np.array([[0,1], 
                                    [np.nan, np.nan], 
                                    [np.nan, np.nan], 
                                    [np.nan, np.nan], 
                                    [np.nan, np.nan], 
                                    [np.nan, np.nan], 
                                    [np.nan, np.nan]]) # [raw points, frac of r6]
        
        for num_dice in range(1, 7):
            self.get_expected_value_rec(num_dice, expected_values)
            print(f"Expected value for {num_dice} dice: {expected_values[num_dice]}")

    def get_expected_value_rec(self, num_dice, evs):
        if evs[num_dice] is not [np.nan, np.nan]:
            return evs[num_dice]
        
        for roll in self.possible_rolls:
            if len(roll) == num_dice - 1:
                for i in range(1, 7):
                    new_roll = roll + (i,)
                    new_roll.sort()

                    possible_plays = self.possible_dice_to_keep(Counter(new_roll))
                    play_values = []
                    for i, play in enumerate(possible_plays):
                        play_values.append([0, 0])
                        updated_num_dice = num_dice
                        
                        for combo in play:
                            play_values[i][0] += POINT_SCORING_COMBINATIONS[combo]
                            updated_num_dice -= len(combo)

                        play_values[i][0] += self.get_expected_value_rec(updated_num_dice, evs)[0]
                        play_values[i][1] += self.get_expected_value_rec(updated_num_dice, evs)[1]

                    


def test():
    evp = ExpectedValuePlayer("ExpectedValuePlayer")
    evp.get_expected_value()