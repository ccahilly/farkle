class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = 0
        self.scores = [0] * len(players)

    def play(self):
        # All players play until one reaches 10,000 points
        while not self.reached_ten_thousand():
            self.execute_one_turn()
        
        first_to_ten_thousand = self.reached_ten_thousand()
        
        # Allow all other players to have one more turn
        while self.current_player != first_to_ten_thousand:
            self.execute_one_turn()

    def execute_one_turn(self):
        player = self.players[self.current_player]
        score = player.take_turn()
        self.scores[self.current_player] += score
        self.current_player = (self.current_player + 1) % len(self.players)

    # Returns the index of the first player to reach 10,000 points
    def reached_ten_thousand(self):
        return self.scores.index(max(self.scores)) if max(self.scores) >= 10000 else -1
    
    def winner(self):
        return self.scores.index(max(self.scores))