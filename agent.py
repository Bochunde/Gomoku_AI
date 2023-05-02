import numpy as np
from MCTS import MCTS
from AlphaZero_Gomoku.game import Board
def policy_value_fn(board:Board)->tuple:
    """a function that takes in a state and outputs a list of (action, probability)
    tuples and a score for the state"""
    # return uniform probabilities and 0 score for pure MCTS
    action_probs = np.ones(len(board.availables))/len(board.availables)
    return zip(board.availables, action_probs), 0

class agent(object):
    """AI player based on MCTS"""
    #order: 1 go first, 2 go second
    def __init__(self,order:int,epsilon=5, n_step=2000):
        self.mcts = MCTS(policy_value_fn, epsilon, n_step)
        self.order = order
    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board:Board):
        sensible_moves = board.availables
        if len(sensible_moves) > 0:
            move = self.mcts.get_move(board)
            self.mcts.update_with_move(-1)
            return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)
    
