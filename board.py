import random
import numpy as np

class GameBoard:
    '''
    This class handles the game board and its validators/checkers
    '''
    X = 1
    O = -1
    EMPTY = 0
    PLAYERS = [X, O]
    PLAYER_DISPLAY = {
        X: 'X',
        O: 'O',
        EMPTY: ' '}

    def __init__(self, rows = 6, cols = 7):
        self.rows = 6
        self.cols = 7
        self.clear()


    @property
    def current_player(self):
        if self.count_tokens(self.X) > self.count_tokens(self.O):
            return self.O
        else:
            return self.X


    @property
    def current_player_str(self):
        return self.PLAYER_DISPLAY[self.current_player]


    @property
    def total_moves(self):
        return self.count_tokens(self.X) + self.count_tokens(self.O)


    def place_token(self, col):
        """Current player makes a move in column index col """
        row, = np.where(self.board[:,col] == 0)
        self.board[row[-1]][col] = self.current_player


    def validate_move(self, col):
        """Returns True if column is a legal move """
        if col not in range(self.cols):
            return False
        return self.board[0][col] == 0


    def get_legal_moves(self):
        """Returns a list of valid column moves """
        return np.where(self.board[0] == self.EMPTY)[0]


    def get_random_move(self):
        """Returns a random move or None if there aren't any """
        moves = self.get_legal_moves()
        if len(moves) == 0:
            return None
        else:
            return np.random.choice(moves)


    def count_tokens(self, player):
        d = {self.X: 0, self.O: 0, self.EMPTY:0}
        for row in self.board:
            for cell in row:
                d[cell] += 1
        return d[player]


    def get_winner(self):
        """Get the player who has won, or None if not over/tie """
        if self.has_won(self.X):
            return self.X
        elif self.has_won(self.O):
            return self.O
        else:
            return None


    def game_over(self):
        """Return true if the game is over """
        return not np.count_nonzero(self.get_legal_moves()) or self.get_winner() != None


    def clear(self):
        """Clear the board to reset the game """
        self.board = np.zeros((self.rows, self.cols), dtype=np.int8)


    def check_cols(self, player):
        for i in range(self.rows-3):
            for j in range(self.cols):
                if (
                    self.board[i][j]   == self.board[i+1][j] == 
                    self.board[i+2][j] == self.board[i+3][j] == 
                    player
                ): return True
        return False


    def check_rows(self, player):
        for i in range(self.rows):
            for j in range(self.cols-3):
                if (
                    self.board[i][j]   == self.board[i][j+1] ==
                    self.board[i][j+2] == self.board[i][j+3] ==
                    player
                ): return True
        return False


    def check_back_diags(self, player): # like this \
        for i in range(self.rows-3):
            for j in range (self.cols-3):
                if (
                    self.board[i][j]     == self.board[i+1][j+1] ==
                    self.board[i+2][j+2] == self.board[i+3][j+3] ==
                    player
                ): return True
        return False


    def check_fwd_diags(self, player): # like this /
        for i in range(self.rows-3):
            for j in range(self.cols-3):
                if (
                    self.board[i+3][j]     == self.board[i+2][j+1] ==
                    self.board[i+1][j+2]   == self.board[i][j+3] ==
                    player
                ): return True
        return False


    def has_won(self, player):
        return (self.check_cols(player) or self.check_rows(player) or 
            self.check_fwd_diags(player) or self.check_back_diags(player))


    def __eq__(self, other):
        return np.all(self.board == other.board)


    def __hash__(self):
        return hash(np.array_str(self.board))


    def __str__(self):
        outstr = ''
        for row in self.board:
            for col in row:
                outstr += '[' + self.PLAYER_DISPLAY[col] + ']'
            outstr += '\n'
        for i in range(self.cols):
            outstr += f" {i+1} "
        return outstr
