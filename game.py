from board import GameBoard
import aiplayer

from itertools import cycle
import sys, random

class Game:
    
    def __init__(self):
        self.board = GameBoard()
        self.verbose = False
        self.winner_count = dict.fromkeys(self.board.PLAYERS + [None], 0)

    def make_move(self, col):
        if not self.board.validate_move(col):
            raise Exception("Invalid move")

        self.board.place_token(col)

    def play_hvh(self):
        """for human v human play """
        while not self.game_over():
            print(self.board)
            print(f"It's {self.board.current_player_str}'s turn. Where would you like to go?\n")
            val = input()
            try:
                col = int(val)-1
                self.make_move(col)
            except:
                print("Not a valid input\0")
                continue
        self.winner_count[self.winner] += 1
    

    def play_AIvH(self, player):
        print("Loading the AI")
        ai = aiplayer.AIPlayer()
        player = True
        while not self.game_over():
            print(self.board)
            if not player: #ai goes
                print(f"It's the AI's [{self.board.current_player_str}] turn.\n")
                move = ai.get_move(self.board)
                self.make_move(move)
            else:
                print("It's your turn. Where would you like to go?\n")
                val = input()
                try:
                    col = int(val)-1
                    self.make_move(col)
                except:
                    print("Not a valid input\0")
                    continue
            player = not player

    def play_AIvAI(self, ai1=None, ai2=None):
        """Make 2 neural nets play each other"""
        print("Loading the models...")
        ai1 = ai1 or aiplayer.AIPlayer()
        ai2 = ai2 or aiplayer.AIPlayer()
        players = cycle([ai1, ai2])
        while not self.game_over():
            player = next(players)
            print(self.board)
            print(f"It's {self.board.current_player_str}'s turn.\n")
            move = player.get_move(self.board)
            self.make_move(move)


    def play_random_game(self, times = 1):
        for _ in range(times):
            self.reset_game()      
            while (not self.game_over()):
                move = self.board.get_random_move()
                self.make_move(move)
            if self.verbose:
                self.print_winning_dialog()
            self.winner_count[self.winner] += 1


    def make_random_moves(self, moves):
        for _ in range(moves):
            if self.game_over():
                break
            move = self.board.get_random_move()
            self.make_move(move)
            

    def reset_game(self):
        self.board.clear()

    def game_over(self):
        return self.board.game_over()

    @property
    def winner(self):
        if not self.game_over():
            return None
        else:
            return self.board.get_winner()

    def display_stats(self):
        total = sum(self.winner_count.values())
        print(f"Total games: {total}")
        for player, wins in self.winner_count.items():
            if player:
                print(f"{player} has won {wins} times ({100*wins/total:.2f}%)")
            else:
                print(f"there have been {wins} ties")

    def print_winning_dialog(self):
        print("=" * self.board.cols)
        print(self.board)
        print("=" * self.board.cols)
        winner = self.winner
        if winner:
            print(f"{self.board.PLAYER_DISPLAY[winner]} has won in {self.board.total_moves} moves!")
        else:
            print(f"Game ended in a tie after {self.board.total_moves} moves")

class GameState:

    def __init__(self, game_board, player):
        self.state = game_board.board
        self.player = game_board.current_player


if __name__ == "__main__":
    game = Game()
    game.verbose = True
    game.play_AIvH(random.choice([True, False]))
    game.print_winning_dialog()

    