import chess
import chess.polyglot
import chess.svg
from random import*
from move_generation import next_move_minmax, next_move_random, Transposition_table
from score_fun import score, easy_score

class Player():

    def __init__(self, strategy, depth=0):
        self.next_moves = [chess.Move.null, chess.Move.null]
        self.strategy = strategy
        self.depth = depth
        self.past_moves = []
        self.scores = []
        self.table = Transposition_table(64)

    def generate_move(self, board):
        if self.strategy == "Minmax":
            move, alpha, next_moves = next_move_minmax(score, self.depth, board, self.table, self.next_moves)
            self.next_moves = next_moves
            self.scores.append(alpha)
            return move
        elif self.strategy == "Random":
            return next_move_random(board)
        else:
            print("Error")
            return None

    def play_move(self, board):
        move = self.generate_move(board)
        self.past_moves.append(move)
        board.push(move)
  
    


def cpu_v_cpu(position):
    turn_count = 0
    is_white_turn = True
    player_1 = Player("Minmax", 4)
    player_2 = Player("Random")

    while not position.is_game_over():
        if turn_count % 2 == 0:
            print("Turn : ",turn_count)

        """ print("White turn", not position.turn)
        print(position)
        input(" ") """
        #first few turns are based from human matches to makes games more random
        if turn_count <= 2 :
            try :
                move = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(position).move
            except : 
                if turn_count % 2 == 1 : move, alpha, rubbish = next_move_minmax(score, 3, position, Transposition_table())
                if turn_count % 2 == 0 : move, alpha, rubbish = next_move_minmax(score, 3, position, Transposition_table())
            finally :
                position.push(move)

        if position.turn:
            player_1.play_move(position)
        else: 
            player_2.play_move(position)

        turn_count +=1

    print(position.outcome())
    print(player_1)
    return position             #white loses
        
""" def disply_last_moves(position, n_moves):
    positions = [position]
    for i in range(0, n_moves):
        position.pop() """


def cpu_v_cpu_stats(N_games):
    n_white_victories = 0
    n_black_victories = 0
    average_end_turn = 0

    for i in range(N_games):
        board = chess.Board(chess.STARTING_FEN)
        if i % 1 == 0:
            print("Game n° ", i)
        pos = cpu_v_cpu(board)
        if pos.outcome().winner : 
            n_white_victories += 1
            print("White wins")
        if not pos.outcome().winner: 
            n_black_victories += 1
            print("Black wins")
            chess.svg.board(pos)
            pos.pop()
            chess.svg.board(pos)
            
    n_white_victories = n_white_victories/N_games * 100
    n_black_victories = n_black_victories/N_games * 100
    print("White won ", n_white_victories, " \% games, black won ", n_black_victories)


cpu_v_cpu_stats(10)
 
""" test = chess.Board(None)

dict = {chess.B7 : chess.Piece(chess.QUEEN, chess.BLACK), chess.A6 : chess.Piece(chess.ROOK, chess.BLACK), 
        chess.H8 : chess.Piece(chess.KING, chess.WHITE)}

test.set_piece_map(dict)
test.turn = chess.BLACK

a = next_move_minmax(score, 4, test)
test.push(a)
a = next_move_minmax(score, 4, test)
print(a)
print(test)
 """