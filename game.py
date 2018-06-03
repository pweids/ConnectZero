'''
This is the main handler for the game.
'''

from board import Board

if __name__ == "__main__":
    board = Board()
    turn = 0

    print("Welcome to the game!\n")
    player = 'X'

    while not board.has_winner():
        player = 'X' if turn % 2 is 0 else 'O'
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
        turn += 1

    print("=" * board.cols)
    print(board)
    print("=" * board.cols)
    print(f"{board.get_winner()} has won!")