from players.bellmanUpdatePlayer import BellmanUpdatePlayer
from math import factorial
from collections import Counter

def unique_orderings(tpl):
    # Count frequencies of each element
    freq = Counter(tpl)
    
    # Compute the numerator (n!)
    n_fact = factorial(len(tpl))
    
    # Compute the denominator (product of k_i!)
    denom = 1
    for count in freq.values():
        denom *= factorial(count)
    
    # Compute the number of unique orderings
    return n_fact // denom

def main():
    player = BellmanUpdatePlayer()
    print("Number of states:", len(player.S))
    total = 0
    for s in player.S:
        if s != "Start" and s != "End":
            total += unique_orderings(s)
    
    assert total == 55988 - 2

    print("Number of actions:", len(player.A))

main()

