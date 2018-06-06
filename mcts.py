import copy
from collections import defaultdict as ddict
import numpy as np


class MCTS:
    
    def __init__(self, c=1.0):
        self.nnet = nnet
        self.c = c # level of exploration. Higher for self-play
        
        # "Each edge stores a set of statistics"
        # We will use a defaultdict for the mappings
        self.Nsa = ddict(int)       # visit count
        self.Wsa = ddict(float)     # total action value
        self.Qsa = ddict(float)     # mean action value
        self.Psa = ddict(float)     # prior probability

        self.Visited = set()


    def search(self, state, nnet):
        # Terminal condition
        if state.game_over(): 
            return -1

        # Not explored condition
        # Use the neural net to predict P(s,*) and V(s)
        if state not in self.Visited:
            P, v = nnet.predict(state)
            self.Update_Psa(state, P)
            self.Visited.add(state)
            return -v

        # Leaf condition
        # 1. Expand the node finding all children/possible moves
        moves = state.get_legal_moves()

        # 2. Choose the best next move based on U(s,a)
        chosen_action = np.argmax([self.U((state, move)) for move in moves])
        chosen_edge = (state, chosen_action)
        next_state = copy.deepcopy(state)
        next_state.place_token(chosen_action)

        # 3. Recursively get the value of the chosen move
        v = self.search(next_state, nnet)
        print(f"Placing in column {chosen_action+1}")

        # 4. Update the edge values to backprop
        self.Nsa[chosen_edge] += 1
        self.Wsa[chosen_edge] += v
        self.Qsa[chosen_edge] = self.Wsa[chosen_edge] / self.Nsa[chosen_edge]
        
        # 5. Return -v because players switch
        print(next_state)
        return -v


    def U(self, edge):
        state = edge[0]
        possible_moves = state.get_legal_moves()
        sum_nsb = sum([self.Nsa[(state, move)] for move in possible_moves])
        explore_factor = self.c * self.Psa[edge] * (np.sqrt(sum_nsb)/(1 + self.Nsa[edge]))
        qsa = self.Qsa[edge]
        return qsa + explore_factor


    def Update_Psa(self, state, P):
        """get all of the moves and update the Psa dict """
        moves = state.get_legal_moves()
        for move in moves:
            self.Psa[(state, move)] = P[move]

    def pi_vec(self, state):
        pi = []
        for action in state.get_legal_moves():
            pi.append(self.Psa[(state, action)])
        return pi