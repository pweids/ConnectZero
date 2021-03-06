from board import GameBoard
from mcts import MCTS
import neural_net, evaluator

import numpy as np
from progress.bar import Bar
from progress.spinner import Spinner

import time, logging, datetime, warnings
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


    def training_session(self, n=80, rounds=1000, turn_time=3):
        """ The neural nets will play the number rounds with
        n games each. The nnets will be trained after every round.
        If the newly trained nnet wins greater than 55% of the time,
        it becomes our new nnet
        """
        self.reset_session()
        start = time.time()
        logging.info(f"==Training session started [{rounds} rounds of {n}]==\n")
        
        fail_count = 0
        oldnnet = deepcopy(self.nnet)

        for rnd in Bar('Epoch').iter(range(rounds)):
            try:
                round_start = time.time()
                logging.info(f" =Round {rnd} started= ")

                self.play_games(n, turn_time)
                
                ev = evaluator.Evaluator(self.nnet, oldnnet)
                win_pct = ev.evaluate()
                if win_pct > 0.55:
                    self.nnet.save_checkpoint()
                    oldnnet = deepcopy(self.nnet)
                    logging.debug(f"Saving trained neural net after {rnd+1} rounds")
                
                logging.info(f" =Round ended in {time.time()-round_start:.2f}s= \n")
                fail_count = 0
                self.tree.reset_tree()
            except KeyboardInterrupt:
                print("Exiting...")
                return
            except Exception as e:
                fail_count += 1
                print_time = datetime.datetime.now()
                self.nnet.save_checkpoint(f'nn_recovery_{print_time}')
                self.tree.save_checkpoint(f'tree_recovery_{print_time}')
                self.reset_session()
                self.nnet = oldnnet
                logging.error(f"\n!!!Error in round {rnd}: {str(e)} [{print_time}]!!!\n")
                if fail_count < 3:
                    continue
                else:
                    logging.error("Failed 3 times in a row. Cancelling...")
                    return

        logging.info(f"==Training session ended in {time.time()-start:.1f}s==\n")


    def play_games(self, n=10, turn_time=1):
        """ This function will n games and store
        the results into the batch variable for training
        """
        winners = defaultdict(int)
        for i in range(n):# Bar('Game', suffix="%(index)d/%(max)d - %(elapsed)ds [%(eta)ds remain]").iter(range(n)):
            winner = self.simulate_game(turn_time)
            winners[winner] += 1
            logging.debug(f"End of game {i}. Winner: {winner}")
            
            self.train()
            self.reset_session()
        for p in winners:
            logging.info(f'{p} has won {winners[p]} times ({winners[p] / n})')


    def simulate_game(self, max_turn_time=1):
        """Simulate a game played by the NeuralNet using the MCTS.
        The tree will stop searching for a turn after max_turn_time (seconds)
        """
        self.board.clear()
        print("\n")
        spinner = Spinner("Playing game...")
        while not self.board.game_over():
            spinner.next()
            start_turn = time.time()
            while (time.time() - start_turn) < max_turn_time:
                self.tree.search(self.board, self.nnet)
            
            pv = self.tree.prob_vec(self.board)
            choose = np.random.choice(len(pv), p=pv)
            self.training_examples.append([deepcopy(self.board), self.tree.pi_vec(self.board), None])
            self.board.place_token(choose)

        self._add_to_results()
        return self.board.get_winner()
       
 
    def train(self):
        # TODO: implement batching
        logging.debug("initiating train...")
        for example in self.training_examples:
            self.nnet.train(*example)


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


    def reset_session(self):
        self.training_examples = []
        self.tree.reset_tree()
        self.board.clear()


if __name__ == "__main__":
    np.seterr(all='warn')
    warnings.filterwarnings('error')
    d = Dojo()
    d.training_session(turn_time=.5)