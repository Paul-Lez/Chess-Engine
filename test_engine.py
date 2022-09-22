import chess
import chess.polyglot
import chess.svg
from random import *
from move_generation import next_move_minmax, next_move_random
from score_fun import score, easy_score

def cpu_v_cpu(position):
    turn_count = 0
    is_white_turn = True
    while not position.is_game_over():
        if turn_count % 50 == 0:
            print("Turn : ",turn_count)  
        """ print("White turn", not position.turn)
        print(position)
        input(" ") """
        #first few turns are based from human matches to makes games more random
        if turn_count <= 2 :
            try :
                move = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(position).move
            except : 
                if turn_count % 2 == 1 : move = next_move_minmax(score, 1, position)
                if turn_count % 2 == 0 : move = next_move_minmax(score, 1, position)
            finally :
                position.push(move)

        if position.turn:
            #print("here")
            move =  next_move_minmax(score, 3, position)
            #print(move)
            position.push(move)
            #print(position)
        else: 
            move = next_move_minmax(easy_score, 1, position) #next_move_random(position)
            #print(score(position))
            position.push(move)


            #print(move)
            #print(- score(position))
            #input(" ")

            #print(position)
        turn_count +=1

    print(position.outcome())
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