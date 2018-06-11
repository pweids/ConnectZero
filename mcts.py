import numpy as np

from collections import defaultdict as ddict
import logging, pickle, copy, os

class MCTS:
    
    def __init__(self, c=1.0):
        self.c = c # level of exploration. Higher for self-play
        
        # "Each edge stores a set of statistics"
        # We will use a defaultdict for the mappings
        self.Nsa = ddict(int)       # visit count
        self.Wsa = ddict(float)     # total action value
        self.Qsa = ddict(float)     # mean action value
        self.Psa = ddict(float)     # prior probability

        self.Visited = set()
        self.Terminals = set()

        logging.basicConfig(filename="mcts.log", level=logging.DEBUG, filemode='w')


    def search(self, state, nnet):
        # Terminal condition
        if state.game_over():
            self.Terminals.add(state)
            return 1 # the "current player" will always be the loser, thus -(-1) = 1

        # Not explored condition
        # Use the neural net to predict P(s,*) and V(s)
        if state not in self.Visited:
            P, v = nnet.predict(state)
            self.Update_Psa(state, P)
            self.Visited.add(state)
            return -v

        # Leaf condition
        # 1. Expand node for all edges (s',*)
        # 2. Choose the best next move based on U(s',a)
        chosen_action = np.argmax(self.U_vec(state))
        chosen_edge = (state, chosen_action)
        next_state = copy.deepcopy(state)
        next_state.place_token(chosen_action)

        # 3. Recursively get the value of the chosen move
        v = self.search(next_state, nnet)
        
        # 4. Update the edge values to backprop
        self.Nsa[chosen_edge] += 1
        self.Wsa[chosen_edge] += v
        self.Qsa[chosen_edge] = self.Wsa[chosen_edge] / self.Nsa[chosen_edge]
        
        # 5. Return -v because players switch
        return -v


    def U_vec(self, state):
        moves = state.get_legal_moves()
        return [self.U((state, move)) if move in moves else -np.inf for move in range(state.cols)]


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


    def prob_vec(self, state):
        prob = []
        moves = state.get_legal_moves()
        for a in range(state.cols):
            if a in moves:
                prob.append(self.Psa[(state, a)])
            else:
                prob.append(0)
        prob /= np.sum(prob) # to normalize in case of rounding error
        return prob


    def pi_vec(self, state): # the temperature gets lower as we get further in the game
        pi = []
        moves = state.get_legal_moves()
        total_visits = np.sum([self.Nsa[(state, move)] for move in moves])
        if total_visits == 0:
            logging.debug("pi_vec total visits was 0")
            return np.ones(state.cols) / state.cols # give them equal probabilities
        for action in range(state.cols):
            edge = (state, action)
            pi.append(self.Nsa[edge] / total_visits)
        return np.array(pi)

    
    def reset_tree(self):
        """Resets the 
        """
        self.Nsa = ddict(int)       
        self.Wsa = ddict(float)     
        self.Qsa = ddict(float)     
        self.Psa = ddict(float)     

        self.Visited = set()
        self.Terminals = set()
    
    def save_checkpoint(self, file="tree_checkpoint.bin"):
        """Save the tree to a checkpoint file for future loading """
        with open(file, 'wb+') as tree_f:
            pickle.dump(self, tree_f)


    @staticmethod
    def load_checkpoint(file="tree_checkpoint.bin"):
        """Load the most recent checkpoint from file. If file does not exits,
        it returns a new tree instead
        """
        if (os.path.isfile(file)):
            with open(file, 'rb') as tree_f:
                return pickle.load(tree_f)
        return MCTS()
