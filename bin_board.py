import random

class Board:
    '''
    This class handles the game board and its validators/checkers
    It uses a binary representation for the board. But ultimately, did not see any speedup
    because array lookup is 1 op and get_player_at is 6 ops, which is the bottleneck.
    String comparison vs int comparison is negligible
    '''
    X = 1
    O = 3
    EMPTY = 0

    def __init__(self, rows = 6, cols = 7):
        self.rows = rows
        self.cols = cols
        self.shifter = (cols*2)*(rows-1) #cached. move to binary index of last row
        self.board = 0


    def place_token(self, col, player):
        for i in self.col_iter(col):
            if self.board & (3 << i) == self.EMPTY:
                self.board |= (player << i)
                return

    def validate_move(self, col):
        # is this a legal move?
        if col >= self.cols:
            return False
        for i in self.col_iter(col):
            if self.board & (3 << i) == 0:
                return True
        return False

    def get_legal_moves(self):
        # each bit is valid or not
        legal = 0
        for col in range(self.cols):
            if self.validate_move(col):
                legal |= 1 << (self.cols-col-1)
        return legal

    def get_random_move(self):
        valids = []
        legals = self.get_legal_moves()
        for i in range(self.cols):
            if bool(legals & (1 << i)):
                valids.append(i)
        return random.choice(valids)

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

    def has_winner(self):
        return self.get_winner() != None

    def check_cols(self, player):
        for i in range(self.rows-3):
            for j in range(self.cols):
                if (
                    self.get_player_at(i,j)   == self.get_player_at(i+1,j) == 
                    self.get_player_at(i+2,j) == self.get_player_at(i+3,j) == 
                    player
                ): return True
        return False
            
    def check_rows(self, player):
        for i in range(self.rows):
            for j in range(self.cols-3):
                if (
                    self.get_player_at(i,j)   == self.get_player_at(i,j+1) ==
                    self.get_player_at(i,j+2) == self.get_player_at(i,j+3) ==
                    player
                ): return True
        return False

    def check_back_diags(self, player): # like this \
        for i in range(self.rows-3):
            for j in range (self.cols-3):
                if (
                    self.get_player_at(i,j)     == self.get_player_at(i+1,j+1) ==
                    self.get_player_at(i+2,j+2) == self.get_player_at(i+3,j+3) ==
                    player
                ): return True
        return False

    def check_fwd_diags(self, player): # like this /
        for i in range(self.rows-3):
            for j in range(self.cols-3):
                if (
                    self.get_player_at(i+3,j)     == self.get_player_at(i+2,j+1) ==
                    self.get_player_at(i+1,j+2)   == self.get_player_at(i,j+3) ==
                    player
                ): return True
        return False

    def col_iter(self, col):
        top_row_bits = col*2
        bottom_row_bits = top_row_bits + self.shifter + 1 #plus 1 because top range is exclusive
        step = 2*self.cols
        return reversed(range(top_row_bits, bottom_row_bits, step))

    def get_player_at(self, row, col):
        index = (col * 2) + (row * 14)
        check_bit = (3 << index) & self.board
        check_bit >>= index
        return check_bit

    def bin_mat(self):
        cell = ''
        row = []
        board = []
        for c in bin(self.board)[2:].zfill(self.rows*self.cols*2):
            cell += c
            if len(cell) == 2:
                row.append(cell)
                cell = ''
            if len(row) == self.cols:
                row.reverse()
                board.append(row)
                row = []
        board.reverse()
        return board

    def __str__(self):
        outstr = ''
        for row in range(self.rows):
            for col in range(self.cols):
                player = self.get_player_at(row, col)
                token = ' '
                if player == self.X:
                    token = 'X'
                elif player == self.O:
                    token = 'O'
                outstr += '[' + token + ']'
            outstr += '\n'
        for i in range(self.cols):
            outstr += f' {i+1} ' 
        return outstr