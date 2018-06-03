import unittest
from board import Board

class TestBoardWinners(unittest.TestCase):

    ''' board to copy for easy visual validation 
    [['', '', '', '', '', '', ''],
    ['', '', '', '', '', '', ''],
    ['', '', '', '', '', '', ''],
    ['', '', '', '', '', '', ''],
    ['', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '']]
    '''
    board = Board()
    def test_empty_board(self):
        board.board = [['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', ''],
                 ['', '', '', '', '', '', '']]
        self.assertFalse(has_won(board, 'X'))
        self.assertFalse(has_won(board, 'O'))

    def test_rows(self):
        board.board = [['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['X', 'X', 'X', 'X', '', '', '']]
        
        board1 = [['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', 'X', 'X', 'X', 'X', ''],
                  ['', '', '', '', 'O', 'O', 'O'],
                  ['', '', '', '', 'O', 'O', 'O'],
                  ['', '', '', '', 'O', 'O', 'O']]
        
        board2 = [['O', 'O', 'O', 'X', 'X', 'X', 'X'],
                  ['', '', '', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', '', '', '', '', '']]
        
        board3 = [['O', 'O', 'O', 'O', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', '', '', 'X', 'X', 'X', 'X']]
        
        board4 = [['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', 'X', 'O', 'X', 'X', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', 'O', 'O', 'O', ''],
                  ['', '', '', '', '', '', '']]

        self.assertTrue(has_won(board0, 'X'))      
        self.assertTrue(has_won(board1, 'X'))      
        self.assertTrue(has_won(board2, 'X'))      
        self.assertTrue(has_won(board3, 'X'))      
        self.assertFalse(has_won(board4, 'X'))

        self.assertFalse(has_won(board0, 'O'))      
        self.assertFalse(has_won(board1, 'O'))      
        self.assertFalse(has_won(board2, 'O'))      
        self.assertTrue(has_won(board3, 'O'))      
        self.assertTrue(has_won(board4, 'O'))  
        
    def test_cols(self):
        board0 = [['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['X', '', '', '', '', '', ''],
                  ['X', '', '', '', '', '', ''],
                  ['X', '', '', '', '', '', ''],
                  ['X', 'O', 'O', 'O', '', '', '']]
        
        board1 = [['', '', '', '', '', '', 'X'],
                  ['', '', '', '', '', '', 'X'],
                  ['', '', 'X', 'X', 'X', '', 'X'],
                  ['', '', '', '', 'O', 'O', 'X'],
                  ['', '', '', '', 'O', 'O', 'O'],
                  ['', '', '', '', 'O', 'O', 'O']]
        
        board2 = [['O', 'O', '', 'X', 'O', 'X', 'X'],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', '', '', '', '', '']]
        
        board3 = [['O', '', 'O', 'O', '', '', ''],
                  ['O', '', '', '', '', '', ''],
                  ['O', '', '', '', '', '', 'X'],
                  ['', '', '', '', '', '', 'X'],
                  ['', '', '', '', '', '', 'X'],
                  ['', '', '', 'O', 'X', 'X', 'X']]
        
        board4 = [['', '', '', '', '', '', ''],
                  ['', '', '', '', '', '', ''],
                  ['', 'X', 'O', 'X', 'X', '', ''],
                  ['', '', 'O', '', '', '', ''],
                  ['', '', 'O', 'X', 'O', 'O', ''],
                  ['', '', 'O', '', '', '', '']]

        self.assertTrue(has_won(board0, 'X'))      
        self.assertTrue(has_won(board1, 'X'))      
        self.assertFalse(has_won(board2, 'X'))      
        self.assertTrue(has_won(board3, 'X'))      
        self.assertFalse(has_won(board4, 'X'))

        self.assertFalse(has_won(board0, 'O'))      
        self.assertFalse(has_won(board1, 'O'))      
        self.assertTrue(has_won(board2, 'O'))      
        self.assertFalse(has_won(board3, 'O'))      
        self.assertTrue(has_won(board4, 'O'))

    def test_fwd_diags(self):
        board0 = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'X', 'O', ' ', ' '],
                [' ', ' ', 'X', 'O', ' ', ' ', ' '],
                [' ', 'X', 'O', ' ', ' ', ' ', ' '],
                ['X', 'O', 'O', 'O', ' ', ' ', ' ']]
        
        board1 = [['', '', '', ' ', ' ', ' ', 'X'],
                  ['', '', '', ' ', ' ', 'X', ' '],
                  ['', '', '', ' ', 'X', ' ', 'O'],
                  ['', '', '', 'X', ' ', 'O', 'X'],
                  ['', '', '', ' ', 'O', 'O', 'O'],
                  ['', '', '', 'O', 'X', 'O', 'O']]
        
        board2 = [['O', 'X', ' ', 'X', 'O', 'X', 'X'],
                [' ', ' ', ' ', 'O', ' ', ' ', ' '],
                [' ', ' ', 'O', ' ', ' ', ' ', ' '],
                [' ', 'O', 'O', ' ', ' ', ' ', ' '],
                [' ', ' ', 'O', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        
        board3 = [['O', ' ', 'O', 'O', ' ', ' ', ' '],
                ['O', 'O', ' ', ' ', ' ', ' ', ' '],
                ['O', ' ', ' ', ' ', ' ', ' ', 'O'],
                [' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', ' ', 'X', 'X'],
                [' ', ' ', ' ', 'O', 'X', 'X', 'X']]
        
        board4 = [[' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', ' ', 'X', ' '],
                [' ', 'X', ' ', 'X', 'X', ' ', ' '],
                [' ', ' ', 'O', ' ', ' ', ' ', ' '],
                [' ', ' ', 'O', 'X', 'O', 'O', ' '],
                [' ', ' ', 'O', ' ', ' ', ' ', ' ']]

        self.assertTrue(has_won(board0, 'X'))      
        self.assertTrue(has_won(board1, 'X'))      
        self.assertFalse(has_won(board2, 'X'))      
        self.assertFalse(has_won(board3, 'X'))      
        self.assertFalse(has_won(board4, 'X'))

        self.assertTrue(has_won(board0, 'O'))      
        self.assertTrue(has_won(board1, 'O'))      
        self.assertTrue(has_won(board2, 'O'))      
        self.assertFalse(has_won(board3, 'O'))      
        self.assertFalse(has_won(board4, 'O'))

    def test_back_diags(self):
        board0 = [['X', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', 'X', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', 'X', 'X', 'O', ' ', ' '],
                  [' ', ' ', 'O', 'X', ' ', ' ', ' '],
                  [' ', 'X', 'O', ' ', ' ', ' ', ' '],
                  ['X', 'O', 'O', 'O', ' ', ' ', ' ']]
        
        board1 = [[' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                  [' ', ' ', ' ', ' ', ' ', 'X', ' '],
                  ['X', ' ', ' ', ' ', 'O', ' ', 'O'],
                  [' ', 'X', ' ', 'X', ' ', 'O', 'X'],
                  [' ', ' ', 'X', ' ', 'O', 'O', 'O'],
                  [' ', ' ', ' ', 'X', 'X', 'O', 'O']]
        
        board2 = [['O', 'X', ' ', 'X', 'O', 'X', 'X'],
                  [' ', ' ', ' ', 'O', ' ', 'X', ' '],
                  [' ', ' ', 'O', 'X', 'O', ' ', ' '],
                  [' ', 'X', 'O', 'X', 'X', 'O', ' '],
                  [' ', ' ', 'O', ' ', ' ', 'X', 'O'],
                  [' ', ' ', ' ', ' ', ' ', ' ', 'X']]
        
        board3 = [['O', ' ', 'O', 'X', ' ', ' ', ' '],
                  ['O', 'O', ' ', ' ', 'X', ' ', ' '],
                  ['O', ' ', ' ', ' ', ' ', 'X', 'O'],
                  [' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                  [' ', ' ', ' ', ' ', ' ', 'X', 'X'],
                  [' ', ' ', ' ', 'O', 'X', 'X', 'X']]
        
        board4 = [[' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                  [' ', ' ', ' ', ' ', ' ', 'X', ' '],
                  [' ', 'X', ' ', 'X', 'X', ' ', ' '],
                  [' ', ' ', 'O', ' ', ' ', ' ', ' '],
                  [' ', ' ', 'O', 'X', 'O', 'O', ' '],
                  [' ', ' ', 'O', ' ', ' ', ' ', ' ']]

        self.assertTrue(has_won(board0, 'X'))      
        self.assertTrue(has_won(board1, 'X'))      
        self.assertTrue(has_won(board2, 'X'))      
        self.assertTrue(has_won(board3, 'X'))      
        self.assertFalse(has_won(board4, 'X'))
  

if __name__ == '__main__':
    unittest.main()