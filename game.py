class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = 0

    def play(self):
        while not self.is_over():
            player = self.players[self.current_player]
            score = player.take_turn()
            self.scores[self.current_player] += score
            self.current_player = (self.current_player + 1) % len(self.players)

    def is_over(self):
        return any(score >= 10000 for score in self.scores)