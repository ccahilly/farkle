from gameConstants import MIN_PLAYERS, PLAYER_TYPES
from players.randomPlayer import RandomPlayer
from players.humanPlayer import HumanPlayer
from game import Game

def main():
    print("Welcome to Farkle!")
    # Get the number of players from the user
    num_players = input("Enter the number of players: ")
    while not num_players.isdigit() or int(num_players) < MIN_PLAYERS:
        num_players = input(f"Please enter a valid number. Must be >= {MIN_PLAYERS}: ")
    num_players = int(num_players)

    # Get the players
    players = []
    
    print("\nPlayer types: ")
    for i, player_type in enumerate(PLAYER_TYPES):
        print(f"{i + 1}. " + player_type)
    
    for i in range(num_players):    
        player_type = input(f"\nEnter the type for player {i + 1}: ")
        while not player_type.isdigit() or int(player_type) not in range(1, len(PLAYER_TYPES) + 1):
            player_type = input(f"Please enter a valid player type. Must be in range [1, {len(PLAYER_TYPES)}]: ")
        player_type = int(player_type) - 1

        if PLAYER_TYPES[player_type] == "Random":
            players.append(RandomPlayer())
        elif PLAYER_TYPES[player_type] == "Human":
            # Get name from user
            name = input(f"Enter the name for player {i + 1}: ")
            players.append(HumanPlayer(name))

    # Start the game
    game = Game(players)
    winner = game.play()
    print(f"The winner is player {winner + 1} ({players[winner].name})!")

main()