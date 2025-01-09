from players.player import Player
from itertools import product
from collections import Counter
from gameConstants import NUM_DICE, POINT_SCORING_COMBINATIONS

class BellmanUpdatePlayer(Player):
    def __init__(self, name="BellmanUpdate"):
        super().__init__(name)
        self.S, self.A = generateStateActionSpace()
        self.gamma = 1
    
    # Probability of transitioning from state s to s_prime given action a
    def T(self, s, a, s_prime):
        dice_kept, roll_again = a

        if s_prime == "Start":
            return 0 # Invalid end state

        if not roll_again:
            return 1 if s_prime == "End" else 0
        
        if s == "End":
            return 1 if s_prime == "End" and dice_kept == () else 0
        
        if s == "Start":
            if s_prime == "End":
                return 0
            elif len(s_prime) == NUM_DICE and dice_kept == ():
                return 6 ** -NUM_DICE
            return 0

        possibilities = self.possible_dice_to_keep(Counter(s))

        # Farkle
        if len(possibilities) == 0:
            return 1 if s_prime == "End" and dice_kept == () else 0
        
        # Can only end if a farkle or not roll_again
        if s_prime == "End":
            return 0

        
        if dice_kept not in self.possible_dice_to_keep(Counter(s)):
            return 0 # invalid action
        
        num_dice_kept = sum(len(dice) for dice in dice_kept)
        if len(s_prime) == NUM_DICE and len(s) - num_dice_kept == 0:
            return 6 ** -NUM_DICE
        elif len(s_prime) == len(s) - num_dice_kept:
            return 6 ** -len(s_prime)
        
        return 0 # Invalid transition
    
    def R(self, s, a):
        dice_kept, _ = a

        if dice_kept in self.possible_dice_to_keep(Counter(s)):
            move_points = 0
            for dice in dice_kept:
                move_points += POINT_SCORING_COMBINATIONS[dice]
            return move_points
        elif 


def generate_dice_rolls(max_dice=6):
    """
    Generate all possible dice rolls for 1 to `max_dice` dice.
    Each die can roll a value between 1 and 6.
    
    Parameters:
        max_dice (int): The maximum number of dice to consider.
        
    Returns:
        dict: A dictionary where keys are the number of dice,
              and values are lists of tuples representing all possible rolls.
    """
    all_rolls = set()
    for num_dice in range(1, max_dice + 1):
        rolls = product(range(1, 7), repeat=num_dice)
        all_rolls.update(rolls)
    return all_rolls

def generateStateActionSpace():
    player = Player(name="Test")

    S = set(["Start", "End"])
    S.update(generate_dice_rolls())

    A = set() # No action, do not roll again
    for i, state in enumerate(S):
        possiblilities = player.possible_dice_to_keep(Counter(state))
        for dice_kept in possiblilities:
            A.add((dice_kept, True))
            A.add((dice_kept, False))
        
        if (i + 1) % 10000 == 0:
            print(f"Processed {i + 1} states")
    
    for action in A:
        assert action[0] != () # Must keep at least one die
    
    A.add(((), False)) # No dice to keep & do not roll again

    return S, A