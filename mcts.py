import copy
from collections import defaultdict as ddict
import numpy as np

class TreeNode:
    
    def __init__(self, state, parent = None):
        self.Q = 0 # the total number of wins for this player
        self.N = 0 # the total times visited
        self.state = state # the GameBoard instance
        self.parent = parent # who created this
        self.children = [] # the children when expanded

    def expand(self):
        moves = self.state.get_legal_moves()
        for move in moves:
            state = copy.deepcopy(self.state)
            state.place_token(i)
            self.children.append(Node(state, self))
    
    @property
    def terminal(self):
        return self.state.game_over()

class MCTS:
    
    def __init__(self, nnet, c=1.0):
        self.nnet = nnet
        self.c = c # level of exploration. Higher for self-play
        
        # "Each edge stores a set of statistics"
        # We will use a defaultdict for the mappings
        self.Nsa = ddict(int) # visit count
        self.Wsa = ddict(float) # total action value
        self.Qsa = ddict(float) # mean action value
        self.Psa = ddict(float) # prior probability
        self.Visited = set()    # the states we've seen

    def search(self, state):
        if state.game_over(): return state.get_win_value()

        moves = state.get_legal_moves()
        best_edge = np.argmax(U(state, move) for move in moves)
        pass

    def U(self, edge):
        state = edge[0]
        possible_moves = state.get_legal_moves()
        sum_nsb = sum([self.Nsa[(state, move)] for move in possible_moves])
        explore_factor = self.c * self.Psa[edge] * (np.sqrt(sum_nsb)/(1 + self.Nsa[edge]))
        return self.Qsa(edge) + explore_factor