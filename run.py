from gameConstants import MIN_PLAYERS, PLAYER_TYPES, VERBOSE
from players.randomPlayer import RandomPlayer
from players.humanPlayer import HumanPlayer
from game import Game

def print_win_rates(win_counts, players):
    print(f"\nWin rates for each player after {sum(win_counts)} games:")
    for i, player in enumerate(players):
        print(f"{player.name}: {win_counts[i] / sum(win_counts):.3f}")

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
            players.append(RandomPlayer(name=f"Random Player {i + 1}"))
        elif PLAYER_TYPES[player_type] == "Human":
            # Get name from user
            name = input(f"Enter the name for player {i + 1}: ")
            players.append(HumanPlayer(name))
    print()

    # Enter the number of games to play
    num_games = input("Enter the number of games to play: ")
    while not num_games.isdigit():
        num_games = input("Please enter a valid number.")
    num_games = int(num_games)

    win_counts = [0] * num_players

    for i in range(num_games):
        # Start the game
        game = Game(players)
        winner = game.play()
        win_counts[winner] += 1
        if VERBOSE:
            print(f"The winner is {players[winner].name}!")

        if (i + 1) % 100 == 0:
            print_win_rates(win_counts, players)

main()