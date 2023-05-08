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
        move = location.split(',')
        try:
            move = move[0]*8+move[1]
            if move > 63 or move < 0 or move not in board.possible_move:
                move = -1
        except:
            move = -1
        if move == -1:
            print("invalid move")
            move = self.get_action(board)
        return move
