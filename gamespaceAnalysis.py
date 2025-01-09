from players.player import Player
from itertools import product
from collections import Counter

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

def main():
    player = Player(name="Test")

    S = set(["Start", "End"])
    S.update(generate_dice_rolls())

    assert len(S) == 55988

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

    print(len(A))

if __name__ == "__main__":
    main()