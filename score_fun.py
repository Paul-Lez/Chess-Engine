import chess
import chess.polyglot
import chess.svg
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
    chess.PAWN: 1000,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

#computes the material score of a given position for each colour
#returns very hight score for mate 
def score(position):
    if position.is_checkmate():
        total_score = float('inf') if position.outcome().winner else -float('inf')
    else:
        #count how many of each piece
        wp = len(position.pieces(chess.PAWN, chess.WHITE)) 
        wk = len(position.pieces(chess.KNIGHT, chess.WHITE)) 
        wb = len(position.pieces(chess.BISHOP, chess.WHITE)) 
        wr = len(position.pieces(chess.ROOK, chess.WHITE)) 
        wq = len(position.pieces(chess.QUEEN, chess.WHITE)) 
        wk = len(position.pieces(chess.KING, chess.WHITE)) 
        bp = len(position.pieces(chess.PAWN, chess.BLACK)) 
        bk = len(position.pieces(chess.KNIGHT, chess.BLACK)) 
        bb = len(position.pieces(chess.BISHOP, chess.BLACK)) 
        br = len(position.pieces(chess.ROOK, chess.BLACK)) 
        bq = len(position.pieces(chess.QUEEN, chess.BLACK))
        bk = len(position.pieces(chess.KING, chess.BLACK)) 

        #each piece gets adds to the score, weighted by its color, type and position on the board.
        material_score = ((wp - bp) * piece_values[chess.PAWN] + (wk - bk) * piece_values[chess.KNIGHT] 
        + (wb - bb) * piece_values[chess.BISHOP] + (wr - br) * piece_values[chess.ROOK] + (wq - bq) * piece_values[chess.QUEEN])
        pwn_score = sum([pawntable[i] for i in position.pieces(chess.PAWN, chess.WHITE)]) 
        - sum([pawntable[chess.square_mirror(i)] for i in position.pieces(chess.PAWN, chess.BLACK)])

        knight_score = sum([knightstable[i] for i in position.pieces(chess.KNIGHT, chess.WHITE)]) - sum([knightstable[chess.square_mirror(i)] for i in position.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_score = sum([bishopstable[i] for i in position.pieces(chess.BISHOP, chess.WHITE)]) - sum([bishopstable[chess.square_mirror(i)] for i in position.pieces(chess.BISHOP, chess.BLACK)])
        rook_score = sum([rookstable[i] for i in position.pieces(chess.ROOK, chess.WHITE)]) - sum([rookstable[chess.square_mirror(i)] for i in position.pieces(chess.ROOK, chess.BLACK)])
        queen_score = sum([queenstable[i] for i in position.pieces(chess.QUEEN, chess.WHITE)]) - sum([queenstable[chess.square_mirror(i)] for i in position.pieces(chess.QUEEN, chess.BLACK)])
        
        total_score = material_score + 0.2*(pwn_score + knight_score + bishop_score + rook_score + queen_score)
        
        #take into account mobility
        this_mobility = position.legal_moves.count()
        position.turn = not position.turn
        mobility_opposite_player = position.legal_moves.count()
        position.turn = not position.turn
        signed_mobility = (this_mobility - mobility_opposite_player if 
                            position.turn else mobility_opposite_player - this_mobility)
    #score += signed_mobility
    if position.turn:
        return total_score
    else:
        return -total_score

def easy_score(position):
    wp = len(position.pieces(chess.PAWN, chess.WHITE)) 
    wk = len(position.pieces(chess.KNIGHT, chess.WHITE)) 
    wb = len(position.pieces(chess.BISHOP, chess.WHITE)) 
    wr = len(position.pieces(chess.ROOK, chess.WHITE)) 
    wq = len(position.pieces(chess.QUEEN, chess.WHITE))
    wk = len(position.pieces(chess.KING, chess.WHITE))  
    bp = len(position.pieces(chess.PAWN, chess.BLACK)) 
    bk = len(position.pieces(chess.KNIGHT, chess.BLACK)) 
    bb = len(position.pieces(chess.BISHOP, chess.BLACK)) 
    br = len(position.pieces(chess.ROOK, chess.BLACK)) 
    bq = len(position.pieces(chess.QUEEN, chess.BLACK)) 
    bk = len(position.pieces(chess.KING, chess.BLACK)) 
    material_score = ((wp - bp) * piece_values[chess.PAWN] + (wk - bk) * piece_values[chess.KNIGHT] 
    + (wb - bb) * piece_values[chess.BISHOP] + (wr - br) * piece_values[chess.ROOK] + (wq - bq) * piece_values[chess.QUEEN]
    + (wk - bk) * piece_values[chess.KING])
    if position.turn:
        return material_score
    else:
        return -material_score


""" test = chess.Board(None)

dict = {chess.B7 : chess.Piece(chess.QUEEN, chess.BLACK), chess.A6 : chess.Piece(chess.ROOK, chess.BLACK), 
        chess.B1 : chess.Piece(chess.KING, chess.BLACK), chess.B3 : chess.Piece(chess.QUEEN, chess.BLACK),
        chess.H8 : chess.Piece(chess.KING, chess.WHITE)}

test.set_piece_map(dict)
test.turn = chess.BLACK

print(test)
print(easy_score(test))
print(score(test)) """