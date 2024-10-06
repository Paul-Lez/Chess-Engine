from game_objects import *

# class Strategy():

#     @abstractmethod
#     def generate_move(self, position): 
#         pass 
        

class Strategy():

    def __init__(self, optim_data) -> None:
        

class Player():

    def __init__(self, strategy, game_position) -> None:
        self.type = None # Human or auto 
        self.strategy = strategy # This is to allow control on the tree search algorithm being used
        self.game_data = GameData(game_position)
    
    def set_game_data(self, game_data):
        self.game_data = game_data

    # the strategy function should take position as input and output a move 
    def generate_move(self):
        return self.strategy(self.game_data.get_position())
    

class TwoPlayerGame(): 

    def __init__(self, player1, player2) -> None:
        self.players = [player1, player2]
        self.NPLAYERS = 2 
        self.turn_count = 0
        
    def turn(self): 
        # It is player1's turn when the turncount is even
        return 1 if self.turn_count % 2 == 0 else 0
    
    def push(self, move):
        self.position.play_move(move)

    # query the current player to get their chosen move
    def query_move(self):
        return self.players[self.turn].generate_position()
        
    def player_move(self) -> None:
        # play current player move
        move = self.query_move()
        self.push(move) 


