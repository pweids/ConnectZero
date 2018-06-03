'''
This is the main handler for the game.
'''

from board import Board
from itertools import cycle

def play_random_game(board):
    board.clear_board()
    turn = cycle([board.X, board.O])
    count = 0      
    while (not board.game_over()):
        player = next(turn)
        move = board.get_random_move()
        board.place_token(move, player)
        count += 1


if __name__ == "__main__":
    board = Board()
    turn = cycle(board.PLAYERS)

    print("Welcome to the game!\n")

    while not board.game_over():
        player = next(turn)
        print(board)
        val = input(f"It's {player}'s turn. Where would you like to go?\n")
        try:
            col = int(val)-1
            if not board.validate_move(col):
                print("Can't go there!\n")
                continue
        except:
            print("Not a valid input\0")
            continue
        board.place_token(col, player)

    print("=" * board.cols)
    print(board)
    print("=" * board.cols)
    winner = board.get_winner()
    if winner:
        print(f"{board.get_winner()} has won!")
    else:
        print("Game ended in a tie")