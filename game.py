from gameConstants import WIN_THRESHOLD, FIRST_TURN_THRESHOLD, VERBOSE, DEBUG

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = 0
        self.scores = [0] * len(players)

    # Plays until there is a winner, and returns the index of the winner.
    def play(self):
        # All players play until one reaches 10,000 points
        while self.reached_win_threshold() == -1:
            self.execute_one_turn()
        
        first_to_ten_thousand = self.reached_win_threshold()
        if VERBOSE:
            print(f"Player {first_to_ten_thousand + 1} ({self.players[first_to_ten_thousand].name}) reached 10,000 points!")
        
        # Allow all other players to have one more turn
        while self.current_player != first_to_ten_thousand:
            self.execute_one_turn()
        
        return self.winner()

    # Executes one turn for the current player
    def execute_one_turn(self):
        player = self.players[self.current_player]
        score = player.take_turn()
        
        # The first turn must be at least 500 points
        if self.scores[self.current_player] > 0 or score >= FIRST_TURN_THRESHOLD:
            if DEBUG:
                print(f"{player.name} scored {score} points")
                print(f"self.scores[self.current_player] > 0: {self.scores[self.current_player] > 0}")
                print(f"score >= FIRST_TURN_THRESHOLD: {score >= FIRST_TURN_THRESHOLD}")
            self.scores[self.current_player] += score
        
        self.current_player = (self.current_player + 1) % len(self.players)

        if VERBOSE:
            for i, player in enumerate(self.players):
                print(f"Player {i + 1} ({player.name}): {self.scores[i]} points")
            print()

    # Returns the index of the first player to reach 10,000 points; -1 otherwise
    def reached_win_threshold(self):
        return self.scores.index(max(self.scores)) if max(self.scores) >= WIN_THRESHOLD else -1
    
    # Returns the index of the player with the highest score
    def winner(self):
        return self.scores.index(max(self.scores))