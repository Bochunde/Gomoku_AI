from chess_board import chessboard
class agent_human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board:chessboard):

        location = input("Your move: ")
        location.replace(" ","")

        try:
            x, y = map(int, location.split(','))
            move = x*8 +y
            if move not in board.possible_move:
                print('invalid move')
                move = self.get_action(board)
        except ValueError:
            print("Invalid input. Please enter two integers separated by a comma.")
            move =-1
        if move == -1:
            print("invalid move")
            move = self.get_action(board)
        return move
