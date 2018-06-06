from board import GameBoard
from mcts import MCTS
import neural_net
import numpy as np
from copy import deepcopy
import time
from progress.bar import Bar

class Dojo:
    """This class will train our neural network through self-play """

    def __init__(self, board=None, nnet=None, mcts=None):
        """Pass the baord class (defaults to GameBoard), the neural net instance
        and the MCTS instance
        """
        self.board = board or GameBoard()
        self.nnet = nnet or neural_net.RandomNeuralNet()
        self.tree = mcts or MCTS(3)

        self.batch = []


    def training_session(self, n=10, rounds=100):
        """ The neural nets will play the number rounds with
        n games each. The nnets will be trained after every round.
        If the newly trained nnet wins greater than 55% of the time,
        it becomes our new nnet
        """
        for round in Bar('Epoch').iter(range(rounds)):
            play_games(n)
            # train the nnet
            # clear the batch
            # simulate 1000 games
            # if > 0.55 win rate, replace nnet
            # store the nnet and tree
        pass


    def play_games(self, n=10):
        """ This function will n games and store
        the results into the batch variable for training
        """
        for _ in Bar('Game').iter(range(n)):
            self.simulate_game()

    
    def simulate_game(self, max_turn_time=1):
        """Simulate a game played by the NeuralNet using the MCTS.
        The tree will stop searching for a turn after max_turn_time (seconds)
        """
        self.board.clear()
        start = time.time()
        while not self.board.game_over():
            start_turn = time.time()
            while (time.time() - start_turn) < max_turn_time:
                self.tree.search(self.board, self.nnet)
            pv = self.tree.prob_vec(self.board)
            choose = np.random.choice(len(pv), p=pv)
            self.board.place_token(choose)
            self.batch.append([deepcopy(self.board), self.tree.pi_vec(self.board), None])
        self.add_to_results()
        

    def add_to_results(self):
        """This function loops backwards through the samples that
        were just added to the batch. It will stop when it finds a
        sample that already has a results value
        """
        winner = self.board.get_winner()
        for sample in reversed(self.batch):
            if sample[2] is not None:
                break
            board = sample[0]
            if board.current_player == winner:
                sample[2] = 1
            elif winner is None: #tie
                sample[2] = 0
            else:
                sample[2] = -1
