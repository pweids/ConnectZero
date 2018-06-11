from mcts import MCTS
import neural_net as nn
import numpy as np
import time

class AIPlayer:
    """This class will handle the move selection for an AI """
    def __init__(self, nnet=None, mcts=None):
        self.mcts = mcts or MCTS(.1)
        self.nnet = nnet or nn.NeuralNet.load_checkpoint()


    def get_move(self, board):
        self.evaluate_moves(board)
        pv = self.mcts.prob_vec(board)
        return np.random.choice(len(pv), p=pv)


    def evaluate_moves(self, state, max_iters=1000, timeout_time=np.inf):
        start = time.time()
        for _ in range(max_iters):
            self.mcts.search(state, self.nnet)
            if time.time() - start > timeout_time:
                break