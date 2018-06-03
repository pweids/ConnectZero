import random

class Board:
    '''
    This class handles the game board and its validators/checkers
    '''
    X = 'X'
    O = 'O'
    EMPTY = ' '
    PLAYERS = [X, O]

    def __init__(self, rows = 6, cols = 7):
        self.rows = 6
        self.cols = 7
        self.clear()

    def place_token(self, col, player):
        for row in reversed(self.board):
            if row[col] == self.EMPTY:
                row[col] = player
                return

    def validate_move(self, col):
        # is this a legal move?
        if col not in range(self.cols):
            return False
        for row in self.board:
            if row[col] == self.EMPTY:
                return True
        return False

    def get_legal_moves(self):
        # todo: change to bitarray
        # each bit is valid or not
        legal = []
        for col in range(self.cols):
            if self.validate_move(col):
                legal.append(col)
        return legal

    def get_random_move(self):
        return random.choice(self.get_legal_moves())

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

    def game_over(self):
        return not self.get_legal_moves() or self.get_winner() != None

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
        self.board = [[self.EMPTY]*self.cols for _ in range(self.rows)]

    def __str__(self):
        outstr = ''
        for row in self.board:
            for col in row:
                outstr += '[' + col + ']'
            outstr += '\n'
        for i in range(self.cols):
            outstr += f' {i+1} ' 
        return outstr