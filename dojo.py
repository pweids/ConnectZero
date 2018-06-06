from game import Game
from board import GameBoard
from mcts import MCTS
import neural_net
from copy import deepcopy

class Dojo:
    """This class will train our neural network through self-play """

    def __init__(self, game=None, nnet=None, mcts=None):
        """Pass the game class (defaults to Game), the neural net instance
        and the MCTS instance
        """
        self.Game = game or Game
        self.nnet1 = nnet1 or neural_net.RandomNeuralNet()
        self.tree = mcts or MCTS()

        self.batch = []


    def training_session(self, n=10, rounds=100):
        """ The neural nets will play the number rounds with
        n games each. The nnets will be trained after every round.
        If the newly trained nnet wins greater than 55% of the time,
        it becomes our new nnet
        """
        for round in range(rounds):
            play_games(n)
            # train the nnet
            # simulate 1000 games
            # if > 0.55 win rate, replace nnet
        pass


    def play_games(self, n=10):
        """ This function will n games and store
        the results into the batch variable for training
        """
        g = self.Game()

        pass