import chess
import chess.polyglot
import chess.svg
from random import *
from score_fun import score, easy_score

class Zobrist_hash():

    def __init__(self, length = 32):
        self.table = [[None] * 12] * 64
        for i in range(0, 64):
            for j in range(0, 12):
                self.table[i][j] = randint(0, 2**length - 1)
        self.is_black_to_move = randint(0, 2**length - 1)

    def eval(self, position):
        h = 0
        if position.turn == chess.BLACK:
            h = h ^ self.is_black_to_move
        for i in range(0, 64):
            if position.piece_at(i) != None:
                h = h ^ (self.table[i][position.piece_at(i).color * 6 + position.piece_at(i).piece_type - 1])
        return h
    
class Transposition_table():

    def __init__(self, length=32):
        self.hash = Zobrist_hash(length)
        self.table = {}

    def add(self, position, score, next_moves):
        self.table[self.hash.eval(position)] = [score, next_moves]

    def retrieve(self, position):
        return self.table[self.hash.eval(position)]

def quiece(score_fun, position, alpha, beta):
    #print("Q search")
    starter = score_fun(position)
    if starter >= beta :
        return beta
    if starter > alpha:
        alpha = starter

    for move in position.legal_moves :
        if position.is_capture(move):
            #print("here")
            position.push(move)
            temp_score = - quiece(score_fun, position, -beta, -alpha)
            position.pop()

            if temp_score >= beta :
                return beta
            if temp_score > alpha :
                alpha = temp_score

    return alpha


""" Negamax tree search. 
    Takes the usual parameters plus next two "optimal" moves as 
    input and outputs score of position plus next two "optimal" moves """
def negamax(score_fun, position, depth, alpha, beta, next_moves, table) : 
    if depth == 0 or position.is_game_over() :
        return (score_fun(position), next_moves) #quiece(score_fun, position, alpha, beta)
    else :
        current_score = -float('inf')
        best_move = chess.Move.null

        #basic move ordering: put the best move first
        possible_moves = [move for move in position.legal_moves if move!= next_moves[0]]  #TODO: try and optimise this 
        if next_moves[0] != chess.Move.null:
            possible_moves.insert(0, next_moves[0])

        for move in possible_moves:
            if position.is_legal(move):
                #print(position.turn)
                position.push(move)
                #print(position.turn)
                try: 
                    temp = table.retrieve(position)[0]
                except KeyError:
                    temp, new_next_moves = negamax(score_fun, position, depth - 1, - beta, - alpha, [next_moves[1], next_moves[0]], table)
                    #table.add(position, temp, new_next_moves)
                temp = - temp
                #if move yields better score, update score and current best move
                if temp > current_score: 
                    current_score = temp
                    best_move = move

                position.pop()

                alpha = max(alpha, current_score)
                if alpha >= beta :
                    return (current_score, [next_moves[1], best_move])  # fail hard beta-cutoff

        return (current_score, [next_moves[1], best_move])

#print(negamax(score, chess.Board(chess.STARTING_FEN), 3, -float('inf'), float('inf'), (None, None)))

""" Searches for the move yielding maximal negamax score. 
    Usual inputs plus two next "optimal" moves as parameters.
    Outputs best moves plus the two following "optimal" moves """
def next_move_minmax(score_fun, depth_var, position, table, next_moves=[chess.Move.null, chess.Move.null]): 
    best_move = chess.Move.null
    alpha = -float('inf')
    beta = float('inf')
    is_fivefold = False
    best_score = -float('inf')
    
    #basic move ordering: put the best move first
    possible_moves = [move for move in position.legal_moves if move!= next_moves[0]]  #TODO: try and optimise this 
    if next_moves[0] != chess.Move.null:
        possible_moves.insert(0, next_moves[0])

    for move in possible_moves:
        if position.is_legal(move):
            position.push(move)
            try: 
                temp = table.retrieve(position)
                board_value = temp[0]
                new_moves = temp[1]
            except KeyError: 
                board_value, new_moves = negamax(score_fun, position, depth_var - 1, -beta, -alpha, [next_moves[1], next_moves[0]], table)
                table.add(position, board_value, new_moves)
            board_value = - board_value
            #print(board_value)
            #move_scores.append(board_value)
            #print(board_value)
            best_score = max(board_value, best_score)
            is_fivefold = position.is_fivefold_repetition()
            position.pop()
            #print(board_value)
            #if position.fullmove_number > 50:
                #print(move_scores)
            #print(move, board_value, board_value >= alpha)
            if best_score >= alpha and (not is_fivefold) :
                best_move = move
                alpha = board_value
                best_new_moves = new_moves
                #print("here", alpha)
            if alpha >= beta:    #beta cut-off
                return (best_move, alpha, best_new_moves)
        print(best_score)
    return (best_move, alpha, best_new_moves)

#print(next_move_minmax(score, 3, chess.Board(chess.STARTING_FEN), Transposition_table()))

def next_move_random(position): 
    moves = [move for move in position.legal_moves]
    rand = randint(1, len(moves))
    move = moves[rand-1]
    position.push(move)
    if (not position.is_fivefold_repetition()) or len(moves) == 1:
        position.pop()
        return move
    else: 
        position.pop()
        return next_move_random(position)
    
        
    
