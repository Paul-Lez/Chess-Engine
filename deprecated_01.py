import chess
from random import *

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

piece_values = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}


board = chess.Board(chess.STARTING_FEN)

"""
for square in chess.SQUARES:
    piece = board.piece_at(square)
    print(piece)
    if not piece:
        continue
    if piece.color == chess.WHITE:
        white_material += piece_values[piece.piece_type]
    else:
        black_material += piece_values[piece.piece_type]
"""
#computes the material score of a given position for each colour
#returns very hight score for mate (forgot to implement that in previous version of the function...)
def score(position):
    white_material = 0
    black_material = 0
    if position.is_game_over():
        if position.turn:
            return float('inf')
        else :
            return -float('inf')
    else :  
        wp = len(board.pieces(chess.PAWN, chess.WHITE)) 
        wk = len(board.pieces(chess.KNIGHT, chess.WHITE)) 
        wb = len(board.pieces(chess.BISHOP, chess.WHITE)) 
        wr = len(board.pieces(chess.ROOK, chess.WHITE)) 
        wq = len(board.pieces(chess.QUEEN, chess.WHITE)) 
        bp = len(board.pieces(chess.PAWN, chess.BLACK)) 
        bk = len(board.pieces(chess.KNIGHT, chess.BLACK)) 
        bb = len(board.pieces(chess.BISHOP, chess.BLACK)) 
        br = len(board.pieces(chess.ROOK, chess.BLACK)) 
        bq = len(board.pieces(chess.QUEEN, chess.BLACK)) 

        material_score = (wp - bp) * piece_values[chess.PAWN] + (wk - bk) * piece_values[chess.KNIGHT] + (wb - bb) * piece_values[chess.BISHOP] + (wr - br) * piece_values[chess.ROOK] + (wq - bq) * piece_values[chess.QUEEN]
        
        return material_score

def quiece(position, alpha, beta, player) :
    return score(position)

def minmax(position, depth, alpha, beta, nextPlayer) : 
    if depth == 0 or position.is_game_over() :
        return quiece(position, alpha, beta, nextPlayer)  
    else :
        if nextPlayer:
            value = -float('inf')
            for move in position.generate_legal_moves():
                position.push(move)
                value = max(minmax(position, depth - 1, alpha, beta, False), value)
                position.pop()
                if value >= beta:
                    break #beta cutoff ?
                alpha = max(alpha, value)
            return value 
        else :
            value = float('inf')
            for move in position.generate_legal_moves():
                position.push(move)
                value = min(minmax(position,depth - 1, alpha, beta, True), value)
                position.pop()
                if value <= alpha:
                    break #alpha cutoff
                beta = min(beta, value)
            return value

depth_var = 3

def next_move_minmax(position, maximizer): 
    best_move_score = -float('inf')
    best_move = None
    for move in position.generate_legal_moves():
        position.push(move)
        if maximizer and best_move_score <= minmax(position, depth_var, -float('inf'), float('inf'),  True) :
            best_move = move
        if (not maximizer) and best_move_score >= minmax(position, depth_var, -float('inf'), float('inf'), True) :
            best_move = move
        position.pop()
    print(move)
    return move

def next_move_random(position): 
    rand = randint(1, position.legal_moves.count())
    ct = 1
    for move in position.generate_legal_moves():
        if ct == rand:
            return move
        ct += 1

def cpu_v_cpu(position):
    turn_count = 0
    is_white_turn = True
    while not position.is_game_over():
        print("Turn : ",turn_count)
        turn_count += 1
        if is_white_turn:
            position.push(next_move_random(position))
            is_white_turn = False
        else: 
            position.push(next_move_minmax(position, False))
            is_white_turn = True
            print(position)
            input(" ")

    if is_white_turn:
        (True, turn_count)
    else: 
        (False, turn_count)

def cpu_v_cpu_stats(N_games):
    n_white_victories = 0
    n_black_victories = 0
    average_end_turn = 0
    for i in range(N_games):
        board = chess.Board(chess.STARTING_FEN)
        (is_white, ct) = cpu_v_cpu(board)
        if is_white : n_white_victories += 1
        if not is_white: n_black_victories += 1
        average_end_turn += ct
    n_white_victories = n_white_victories/N_games * 100
    n_black_victories = n_black_victories/N_games * 100
    average_end_turn = average_end_turn/N_games
    print("White won ", n_white_victories, " \% games, black won ", n_black_victories, " \% games. Average number of turns to win was ", average_end_turn)


#cpu_v_cpu_stats(10)
print(cpu_v_cpu(board))

