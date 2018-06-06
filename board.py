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
        row, = np.where(self.board[:,col] == 0)
        self.board[row[-1]][col] = self.current_player

    def validate_move(self, col):
        # is this a legal move?
        if col not in range(self.cols):
            return False
        return col in self.get_legal_moves()

    def get_legal_moves(self):
        return np.where(self.board[0] == self.EMPTY)[0]

    def get_random_move(self):
        moves = self.get_legal_moves()
        if len(moves) == 0:
            return 0
        else:
            return np.random.choice(moves)

    def count_tokens(self, player):
        d = {self.X: 0, self.O: 0, self.EMPTY:0}
        for row in self.board:
            for cell in row:
                d[cell] += 1
        return d[player]

    def has_won(self, player):
        # has somebody won?
        return (self.check_cols(player) or self.check_rows(player) or 
            self.check_fwd_diags(player) or self.check_back_diags(player))

    def get_winner(self):
        if self.has_won(self.X):
            return self.X
        elif self.has_won(self.O):
            return self.O
        else:
            return None

    def get_win_value(self):
        winner = state.get_winner()
        if winner is None:
            return 0
        player = state.current_player
        if winner is player:
            return -1 #because the current player is the next player/loser
        else:
            return 1

    def game_over(self):
        return not np.count_nonzero(self.get_legal_moves()) or self.get_winner() != None

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

    def clear(self):
        self.board = np.zeros((self.rows, self.cols), dtype=np.int8)

    def board_to_int(self):
        board = 0
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                index = i*14 + j*2
                if cell == self.X:
                    board |= 1 << index
                elif cell == self.O:
                    board |= 3 << index
        return board

    def int_to_board(self, bin_board):
        row = []
        board = []
        for i in range(self.rows):
            for j in range(self.cols):
                index = i*14 + j*2
                checkval = ((3 << index) & bin_board) >> index
                if checkval == 1:
                    row.append(self.X)
                elif checkval == 3:
                    row.append(self.O)
                else:
                    row.append(self.EMPTY)
            board.append(row)
            row = []
        return board

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
            outstr += f' {i+1} ' 
        return outstr