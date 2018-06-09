from board import GameBoard
from mcts import MCTS
import neural_net

import numpy as np
from progress.bar import Bar

import time, logging, datetime, sys
from copy import deepcopy
from itertools import cycle
from collections import defaultdict

class Dojo:
    """This class will train our neural network through self-play """

    def __init__(self, board=None, nnet=None, mcts=None, batch_size=10):
        """Pass the baord class (defaults to GameBoard), the neural net instance
        and the MCTS instance
        """
        logging.basicConfig(filename="dojo.log", level=logging.DEBUG,
            filemode='w')

        self.board = board or GameBoard()
        self.nnet = nnet or neural_net.NeuralNet()
        self.tree = mcts or MCTS(3)

        self.training_examples = []
        self.batch_size = batch_size


    def training_session(self, n=15, rounds=1000):
        """ The neural nets will play the number rounds with
        n games each. The nnets will be trained after every round.
        If the newly trained nnet wins greater than 55% of the time,
        it becomes our new nnet
        """
        start = time.time()
        logging.info(f"==Epoch started <{rounds} rounds of {n}==\n")
        
        for rnd in Bar('Epoch').iter(range(rounds)):
            fail_count = 0
            try:
                round_start = time.time()
                logging.info(f" =Round {rnd} started= \n")

                self.play_games(n)
                self.train() # train the nnet
                
                oldnnet = deepcopy(self.nnet)
                win_pct = self.evaluate(self.nnet, oldnnet)
                if win_pct >= 0.55:
                    self.nnet = oldnnet
                    logging.debug(f"Replacing neural net after {rnd+1} rounds")
                
                self._save_checkpoint()
                self.tree.reset_tree()
                logging.info(f" =Round ended in {time.time()-round_start:.2f}s= \n")
                fail_count = 0

            except:
                fail_count += 1
                self.nnet.save_checkpoint(f'nn_recovery_{datetime.datetime.now()}')
                self.tree.save_checkpoint(f'tree_recovery_{datetime.datetime.now()}')
                logging.warning(f"\n!!!Error in round {rnd}: {sys.exc_info()[0]}!!!\n")
                if fail_count < 3:
                    continue
                else:
                    logging.warning("Failed 3 times in a row. Cancelling...")
                    return

        logging.info(f"==Epoch ended in {time.time()-start:.1f}s==\n")


    def play_games(self, n=10):
        """ This function will n games and store
        the results into the batch variable for training
        """
        winners = defaultdict(int)
        for _ in range(n):# Bar('Game', suffix="%(index)d/%(max)d - %(elapsed)ds [%(eta)ds remain]").iter(range(n)):
            winner = self.simulate_game()
            winners[winner] += 1

        for p in winners:
            logging.info(f'{p} has won {winners[p]} times ({winners[p] / n})')


    def simulate_game(self, max_turn_time=.5):
        """Simulate a game played by the NeuralNet using the MCTS.
        The tree will stop searching for a turn after max_turn_time (seconds)
        """
        self.board.clear()
        while not self.board.game_over():
            start_turn = time.time()
            while (time.time() - start_turn) < max_turn_time:
                self.tree.search(self.board, self.nnet)
            
            pv = self.tree.prob_vec(self.board)
            choose = np.random.choice(len(pv), p=pv)
            self.board.place_token(choose)
            self.training_examples.append([deepcopy(self.board), self.tree.pi_vec(self.board), None])

        self._add_to_results()
        return self.board.get_winner()
 
 
    def train(self):
        # TODO: implement batching
        for example in self.training_examples:
            self.nnet.train(*example)


    def evaluate(self, net1, net2, num_games=50, max_turn_time=.2):
        """This function will play two neural nets against
        each other num_games times. It returs the ratio in
        which the first player won
        """
        logging.info("== Starting evaluation round ==")
        p1_wins = 0
        for i in range(num_games):
            game_start = time.time()
            turn = self._get_turn_cycle((net1, MCTS()), (net2, MCTS()))
            self.board.clear()
            while not self.board.game_over():
                start_turn = time.time()
                player = next(turn)
                while (time.time() - start_turn) < max_turn_time:
                    player[1].search(self.board, player[0])
                
                pv = player[1].prob_vec(self.board)
                choose = np.random.choice(len(pv), p=pv)
                self.board.place_token(choose)
            if self.board.get_winner() is net1:
                p1_wins += 1
                logging.info(f"player 1 wins game {i} ({p1_wins} total wins)")
            else:
                logging.info(f"player 2 wins game {i} ({i-p1_wins+1} total wins)")

            logging.debug(f"game {i} took {time.time()-game_start:.1f}s, {self.board.total_moves} moves\n{self.board}")
        return p1_wins/num_games


    def _save_checkpoint(self):
        logging.debug("saving checkpoint...")
        #self.tree.save_checkpoint()
        self.nnet.save_checkpoint()


    def _load_checkpoints(self):
        #self.tree.load_checkpoint()
        self.nnet.load_checkpoint()


    def _add_to_results(self):
        """This function loops backwards through the samples that
        were just added to the batch. It will stop when it finds a
        sample that already has a results value
        """
        winner = self.board.get_winner()
        for sample in reversed(self.training_examples):
            if sample[2] is not None:
                break
            board = sample[0]
            if board.current_player == winner:
                sample[2] = 1
            elif winner is None: #tie
                sample[2] = 0
            else:
                sample[2] = -1


    def _get_turn_cycle(self, *args):
        temp = list(args)
        np.random.shuffle(temp)
        return cycle(temp)


if __name__ == "__main__":
    d = Dojo()
    d.play_games(1)
    d.train()