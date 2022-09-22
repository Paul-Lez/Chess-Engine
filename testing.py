from turtle import position
import chess
import chess.polyglot
import chess.svg
from random import *
from score_fun import score, easy_score
from move_generation import negamax
from deprecated_01 import minmax_alpha_beta, minmax
import time
from move_generation import next_move_minmax

#test minmax and negamax
board = chess.Board(chess.STARTING_FEN)

depth = 4

""" print(negamax(easy_score, board, depth, -float('inf'), float('inf')))
print(minmax(board, depth)) """

dict = {chess.A7 : chess.Piece(chess.QUEEN, chess.BLACK), chess.A6 : chess.Piece(chess.ROOK, chess.BLACK), 
        chess.B1 : chess.Piece(chess.KING, chess.BLACK),
        chess.H8 : chess.Piece(chess.KING, chess.WHITE)}

board.set_piece_map(dict)
board.turn = chess.BLACK 

""" time1 = time.time()
u = negamax(easy_score, board, depth, -float('inf'), float('inf'))
time2 = time.time()
v = minmax(board, depth)
time3 = time.time()
print("Negamax", u, "Minmax", v)
print(time2 - time1, time3 - time2)  """

print(board)
move = (next_move_minmax(score, depth, board))
print(move)
board.push(move)
print(" ")
print(board)
move = (next_move_minmax(score, depth, board))
board.push(move)
print(" ")
print(board)
for move in board.legal_moves:
    board.push(move)
    print(move, -negamax(score, board, depth-1, -float('inf'), float('inf')))
    board.pop()
move = (next_move_minmax(score, depth, board))
print(move)
board.push(move)
print(" ")
print(board)
"""print(board.legal_moves)
move = (next_move_minmax(easy_score, depth, board))
board.push(move)
print(" ")
print(board)
move = (next_move_minmax(score, depth, board))
board.push(move)
print(" ")
print(board)
move = (next_move_minmax(score, depth, board))
board.push(move)
print(" ")
print(board)
move = (next_move_minmax(score, depth, board))
board.push(move)
print(" ")
print(board)
move = (next_move_minmax(score, depth, board))
board.push(move)
print(" ")
print(board)  """



