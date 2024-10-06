from game_objects import *

## This files defines an AbstractGame object for testing the Game library 

# At each turn of the game, the player whose turn it is chooses a number between 1 and N (at most 9).
# The game state is stored as a pair of numbers (S, n_turns), and the update rule is 
# S <- S + 10^n_turns*i and n_turn += 1, where i is the number chosen by the player
# the game ends if the number is even or the sum of the digits of the number is a multiple of 7

class NumbersGame(AbstractGame):

    def __init__(self, N, M) -> None:
        self.N = N
        self.M = M

    def generate_legal_moves(self, position):
        if not self.ended(position):
            return [i for i in range(0, self.N)]
        else:
            return []
    
    def update_position(self, position, move):
        return position[0] + 10^position[1]*move, position[1]+1
    
    def ended(self, position):
        return (position[0] % 2 == 0 or sum(list(map(int, str(position[0])))) % self.M == 0)
    

#### Test ####
game = NumbersGame(3, 8)
position = GamePosition(game, (1, 0))
game_data = GameData(position)
print(game_data.generate_legal_moves())
game_data.update_move_tree(5) 
traverse_print(game_data.move_tree)

