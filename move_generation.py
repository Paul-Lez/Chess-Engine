import chess
import chess.polyglot
import chess.svg
from random import *
from score_fun import score, easy_score

def quiece(score_fun, position, alpha, beta) :
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

def negamax(score_fun, position, depth, alpha, beta) : 
    if depth == 0 or position.is_game_over() :
        return score_fun(position) #quiece(score_fun, position, alpha, beta)
    else :
        current_score = -float('inf')                  
        for move in position.legal_moves :
            if position.is_legal(move):
                #print(position.turn)
                position.push(move)
                #print(position.turn)
                temp = - negamax(score_fun, position, depth - 1, - beta, - alpha )
                current_score = max(current_score, temp)
                position.pop()
                alpha = max(alpha, current_score)
                if alpha >= beta :
                    return current_score  # fail hard beta-cutoff
        return current_score

def next_move_minmax(score_fun, depth_var, position): 
    best_move = chess.Move.null
    alpha = -float('inf')
    beta = float('inf')
    is_fivefold = False
    best_score = -float('inf')
    for move in position.legal_moves:
        position.push(move)
        board_value = - negamax(score_fun, position, depth_var - 1, -beta, -alpha)
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
            #print("here", alpha)
        if alpha >= beta:    #beta cut-off
            return best_move
    return best_move

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