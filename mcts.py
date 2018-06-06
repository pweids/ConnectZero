import copy

class Node:
    
    def __init__(self, state, parent = None):
        self.Q = 0 # the total number of wins for this player
        self.N = 0 # the total times visited
        self.state = state # the GameBoard instance
        self.parent = parent # who created this
        self.children = [] # the children when expanded

    def expand(self):
        moves = self.state.get_legal_moves()
        for i in range(len(moves)):
            if moves[i]: # moves is a t/f array
                state = copy.deepcopy(self.state)
                state.place_token(i)
                self.children.append(Node(state, self))
    
    @property
    def terminal(self):
        return self.state.game_over()

class MCTS:
    pass