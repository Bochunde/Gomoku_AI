import numpy as np
from MCTS import MCTS
from AlphaZero_Gomoku.game import Board
from chess_board import chessboard
def policy_value_fn(board:chessboard)->tuple:
    """a function that takes in a state and outputs a list of (action, probability)
    tuples and a score for the state"""
    # return uniform probabilities and 0 score for pure MCTS
    action_probs = np.ones(len(board.possible_move))/len(board.possible_move)
    return zip(board.possible_move, action_probs), 0

class agent(object):
    """MCTS not using NN"""
    def __init__(self,epsilon=5, n_step=2000):
        self.mcts = MCTS(policy_value_fn, epsilon, n_step)

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board:chessboard):
        sensible_moves = board.possible_move
        if len(sensible_moves) > 0:
            move = self.mcts.get_move(board)
            self.mcts.update_with_move(-1)
            return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)
    
