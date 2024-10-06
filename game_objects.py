from tree_search import *
from abc import ABC, abstractmethod

def tree_gen(board, color, depth):
    return None 

class AbstractGame():

    @abstractmethod
    def update_position(self, position, move):
        pass

    @abstractmethod
    def generate_legal_moves(self, position): 
        pass

    @abstractmethod
    def ended(self, position):
        """
        Return true is game described by the position is finished
        """
        pass

    @abstractmethod
    def init(self): 
        # return starting position.
        pass

    def generate_move_tree(self, position, depth):
        # generate the tree of possible moves following a given position
        # The tree is constructed using the TreeNode class, and each 
        # node has value the position 
        if depth==0:
            return TreeNode(position, []) 
        else: 
            moves = self.generate_legal_moves(position)
            children = []
            for m in moves:
                new_position = self.update_position(position, m) 
                children.append(self.generate_move_tree(new_position, depth-1))
            return TreeNode(position, children)
        
    def extend_move_tree(self, move_tree_root, depth): 
        # extends a move tree so that it has the depth given as the parameter 
        if depth==0: 
            return move_tree_root
        else: 
            if move_tree_root.is_terminal(): 
                return self.generate_move_tree(move_tree_root.value, depth)
            else: 
                new_children = []
                for m in move_tree_root.children:
                    new_children.append(self.extend_move_tree(m, depth-1))
                return TreeNode(move_tree_root.value, new_children)


# A class that captures the notion of a game in play. Store position data, move generation rules and 
# move updating rules
class GamePosition():

    def __init__(self, abstract_game, position=None) -> None:
        self.abstract_game = abstract_game
        if position == None: 
            self.position = self.set_starting_position()
        else: 
            self.position = position
        

    def play_move(self, move) -> None: 
        self.position = self.abstract_game.update_position(self.position, move)

    def generate_legal_moves(self): 
        return self.abstract_game.generate_legal_moves(self.position)
    
    def set_starting_position(self): 
        self.position = self.abstract_game.init()
        

# the class GameData stores: current position, plus tree containing possible next moves
# this probably doesn't need to be an abstract class
class GameData():

    def __init__(self, game, move_tree=None, depth=0) -> None:
        self.game = game
        if move_tree==None :
            self.move_tree = TreeNode(game.position, [])
        else: 
            self.move_tree = move_tree

    # update tree storing next moves to 
    # DO WE WANT TO KEEP CONTROL OF DEPTH OR SHOULD THIS CLASS ALSO KEEP TRACK OF SUCH DATA?
    def update_move_tree(self, depth) -> None: 
        self.move_tree = self.game.abstract_game.extend_move_tree(self.move_tree, depth)

    def generate_legal_moves(self):
        return self.game.generate_legal_moves()
    
    def get_position(self):
        return self.game.position
    
    # THIS CURRENTLY DOES NOT UPDATE THE MOVE TREE (IS THIS SOMETHING WE WANT?)
    def play_move(self, move) -> None: 
        """
        This should 
        1) Update the game position
        ") Update the moves tree
        """
        self.game.play_move(move)
        #self.update_move_tree()



#tricky part here: we need the node evaluation function to work - does this mean we need to remember the path to get to each node?
#probably means that the nodes in the move tree can't only store the move with no other contextual information
#solution: store both the move plus the board position?

def gen_next_move(game_data, optim_dat, depth, color):
    node = game_data.moves
    best_child, _ = get_best_child(node, optim_dat, depth, color)
    return best_child 