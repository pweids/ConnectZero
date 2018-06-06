from mcts import MCTS
import numpy as np
import time

class AIPlayer:
    """This class will handle the move selection for an AI """
    def __init__(self, nnet, mcts=None):
        self.mcts = mcts or MCTS()
        self.nnet = nnet


    def get_move(self, game):
        board = game.board
        self.evaluate_moves(board)
        pi = self.mcts.pi_vec(board)
        # TODO
        pass


    def evaluate_moves(self, state, max_iters=5000, timeout_time=0.5):
        start = time.time()
        for _ in range(max_iters):
            self.mcts.search(state, self.nnet)
            if time.time() - start > timeout_time:
                break