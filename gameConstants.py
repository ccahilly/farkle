NUM_DICE = 6
MIN_PLAYERS = 2
WIN_THRESHOLD = 10000
FIRST_TURN_THRESHOLD = 500
POINT_SCORING_COMBINATIONS = {(1,): 100, 
                              (5,): 50, 
                              (1, 1, 1): 300, 
                              (2, 2, 2): 200, 
                              (3, 3, 3): 300, 
                              (4, 4, 4): 400, 
                              (5, 5, 5): 500, 
                              (6, 6, 6): 600, 
                              (1, 2, 3, 4, 5, 6): 1500,
                              }

# Four of a kind 
for i in range(1, NUM_DICE + 1):
    POINT_SCORING_COMBINATIONS[(i, i, i, i)] = 1000

# Five of a kind
for i in range(1, NUM_DICE + 1):
    POINT_SCORING_COMBINATIONS[(i, i, i, i, i)] = 2000

# Six of a kind
for i in range(1, NUM_DICE + 1):
    POINT_SCORING_COMBINATIONS[(i, i, i, i, i, i)] = 3000

# Three pairs
for i in range(1, NUM_DICE + 1):
    for j in range(i + 1, NUM_DICE + 1):
        for k in range(j + 1, NUM_DICE + 1):
            POINT_SCORING_COMBINATIONS[(i, i, j, j, k, k)] = 1500

# Four of a kind and a pair
for i in range(1, NUM_DICE + 1):
    for j in range(1, NUM_DICE + 1):
        if i != j:
            roll = [i, i, i, i, j, j]
            roll.sort()
            roll = tuple(roll)
            POINT_SCORING_COMBINATIONS[roll] = 1500

# Two triples
for i in range(1, NUM_DICE + 1):
    for j in range(i + 1, NUM_DICE + 1):
        POINT_SCORING_COMBINATIONS[(i, i, i, j, j, j)] = 2500

PLAYER_TYPES = ["Random", "Human"]
VERBOSE = True
DEBUG = True