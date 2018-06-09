from mcts import MCTS
from board import GameBoard

import numpy as np

from random import shuffle
from itertools import cycle
import logging, time

class Evaluator:

    def __init__(self, net1, net2):
        self.p1 = net1
        self.p2 = net2
        

    def evaluate(self, num_games=20, max_turn_time=.2):
        """This function will play two neural nets against
        each other num_games times. It returs the ratio in
        which the first player won
        """
        logging.info("== Starting evaluation round ==")
        p1_wins = 0
        for i in range(num_games):
            players = [(self.p1, MCTS(.5)), (self.p2, MCTS(.5))]
            board = GameBoard()
            
            shuffle(players)
            turn = cycle(players)
            
            game_start = time.time()
            
            while not board.game_over():
                player = next(turn)
                
                start_turn = time.time()
                while (time.time() - start_turn) < max_turn_time:
                    player[1].search(board, player[0])
                
                pv = player[1].prob_vec(board)
                choose = np.random.choice(len(pv), p=pv)
                board.place_token(choose)
                
            if player[0] is self.p1:
                p1_wins += 1
                logging.info(f"player 1 wins game {i} ({p1_wins} total wins)")
            else:
                logging.info(f"player 2 wins game {i} ({i-p1_wins+1} total wins)")
            logging.debug(f"game {i} took {time.time()-game_start:.1f}s, {board.total_moves} moves\n{board}")
            
            if p1_wins/num_games >= 0.55: # end early if p1 has majority
                return 1
            elif (i-p1_wins+1)/num_games >= 0.55:
                return 0
        return p1_wins/num_games