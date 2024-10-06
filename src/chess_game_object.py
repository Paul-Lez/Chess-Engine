from game_objects import *
import copy 

# A concrete class capturing the rules of chess
class ChessGame(AbstractGame):

    def generate_legal_moves(self, position):
        return position.legal_moves
    
    def update_position(self, position, move):
        new_pos = copy.deepcopy(position)
        new_pos.push(move)
        return new_pos

    def ended(self):
        return self.position.is_game_over()
    
