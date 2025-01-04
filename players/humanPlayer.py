from .player import Player

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name=name)
    
    def pick_dice_to_keep(self, roll):
        possibilities = self.possible_dice_to_keep(roll)
        for i, possibility in enumerate(possibilities):
            print(f"{i + 1}. {possibility}")
        
        choice = input("Enter the index of the dice to keep: ")
        while not choice.isdigit() or int(choice) not in range(1, len(possibilities) + 1):
            choice = input(f"Please enter a valid index. Must be in range [1, {len(possibilities)}]: ")
        choice = int(choice) - 1
        
        return list(possibilities)[choice]
    
    def roll_again(self):
        return True if input("Roll again? (y/n): ").lower() == "y" else False