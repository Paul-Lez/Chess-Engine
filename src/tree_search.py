class TreeNode():

    def __init__(self, value, children_array=[]):
        self.value = value 
        self.children = children_array
    
    def add_child(self, child):
        self.children.append(child)

    def is_terminal(self):
        return True if not self.children else False
    
def traverse_print(root_node):
    print(root_node.value)
    for c in root_node.children:
        traverse_print(c)


## is this useful? Currently just a wrapper for TreeNode...
class Tree():

    def __init__(self, root):
        self.root = root 


class Transposition_table():

    def __init__(self, hash):
        self.hash = hash
        self.table = {}

    def add(self, position, score, next_moves):
        self.table[self.hash.eval(position)] = [score, next_moves]

    def retrieve(self, position):
        return self.table[self.hash.eval(position)]
    
class OptimisationDatum():
    """
    OptimisationDatum is a class storing the data necessary to do the tree search: the score function for nodes, a transposition table, the tree search algorithm in use and quiescence search (Do we want Q-search for any game? Presumably we can just declare any leaf position to be safe for games where we don't want Q-search)
    """
    def __init__(self, search_algorithm, score_fun, transposition_table, quiece) :
        self.search_algorithm = search_algorithm
        self.score_fun = score_fun
        self.transposition_table = transposition_table
        self.quiece = quiece 

    ## TODO: this should incorporate the transposition table and the quiescence
    def eval(self, node): 
        return self.score_fun(node)
    
    ## TODO: we also want to allow single player games so this should *not* depend on the player 
    ## i.e. this is something that the node should be able to capture?
    ## Note that we should also be also to vary the tree search method i.e. not 
    ## always use negamax
    def get_best_child(self, node, depth):
        """
        get_best_child(node, optim_dat, depth, color) traverses the tree to depth given by variable depth to find the child node 
        of the starting node that gives the largest score. 
        """
        best_score = -float('inf')
        best_child = None
        # iterate through all the children of the start node
        for child in node.children:
            # negative sign bacause this is negamax and value is being computed wrt the opponent.
            value = self.search_algorithm(child, self.score_fun, self.transposition_table, self.quiece, depth-1)
            # if the current move is better than the one being stored, update the stored move.
            if best_score < value:
                best_child = child 
                best_score = value
        return (best_child, best_score)


# For search_algorithm in the object above we need a version of negamax for "evaluation"
# This implementation of negamax assumes that the nodes store which player is doing the search.
def basic_negamax(node, optim_dat, depth, color):
    if depth == 0 or node.is_terminal():
        return optim_dat.eval(node)
    value = -float('inf')
    for child in node.children:
        value = max(value, -negamax(child, optim_dat, depth-1, not color))
    return value

## We need a version of negamax that is more adapted to optimising tree search:
## the current version only returns the best value, but ideally this should also
## return information about the "path" that was taken
def evaluation_negamax(node, score_fun, transposition_table, quiece, depth):
    if depth == 0 or node.is_terminal():
        return 
    


# Possibly deprecated next move generator.
"""
def get_best_child(node, depth):
    best_score = -float('inf')
    best_child = None
    # iterate through all the children of the start node
    for child in node.children:
        # negative sign bacause this is negamax and value is being computed wrt the opponent.
        value = -negamax(child, optim_dat, depth-1, not color)
        # if the current move is better than the one being stored, update the stored move.
        if best_score < value:
            best_child = child 
            best_score = value
    return (best_child, best_score)


"""

#### Checks ###

n1 = TreeNode(1)
n2 = TreeNode(2)
n3 = TreeNode(-4)
n4 = TreeNode(-15)
n5 = TreeNode(-10)
n6 = TreeNode(4)
n7 = TreeNode(-3)
n8 = TreeNode(45)
n9 = TreeNode(-60)
n10 = TreeNode(90)
n11 = TreeNode(70)
n12 = TreeNode(40)
n13 = TreeNode(-2)
n14 = TreeNode(-7)

n1.add_child(n2)
n1.add_child(n3)
n1.add_child(n4)
n2.add_child(n5)
n2.add_child(n6)
n3.add_child(n7)
n4.add_child(n8)
n3.add_child(n11)
n4.add_child(n12)
n4.add_child(n13)


"""
       n6
      /
n1--n2-n5 
| \
|  \    
|   n3-n7 
|     \
|      n11
-----n4-n8
 

"""


def score(node):
    return node.value

dat = OptimisationDatum(score, None, None)

print(negamax(n1, dat, 1, True))
print(negamax(n1, dat, 0, True))
print(negamax(n1, dat, 2, True))
print(get_best_child(n1, dat, 2, True)[0].value)
