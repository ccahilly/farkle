from gameConstants import WIN_THRESHOLD, FIRST_TURN_THRESHOLD

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = 0
        self.scores = [0] * len(players)

    def play(self):
        # All players play until one reaches 10,000 points
        while self.reached_win_threshold() == -1:
            self.execute_one_turn()
        
        first_to_ten_thousand = self.reached_win_threshold()()
        
        # Allow all other players to have one more turn
        while self.current_player != first_to_ten_thousand:
            self.execute_one_turn()

    # Executes one turn for the current player
    def execute_one_turn(self):
        player = self.players[self.current_player]
        score = player.take_turn()
        
        # The first turn must be at least 500 points
        if self.scores[self.current_player] > 0 or score >= FIRST_TURN_THRESHOLD:
            self.scores[self.current_player] += score
        
        self.current_player = (self.current_player + 1) % len(self.players)

    # Returns the index of the first player to reach 10,000 points; -1 otherwise
    def reached_win_threshold(self):
        return self.scores.index(max(self.scores)) if max(self.scores) >= WIN_THRESHOLD else -1
    
    def winner(self):
        return self.scores.index(max(self.scores))