from MCTS import MCTS
import numpy as np
from chess_board import chessboard
class agent_AI(object):
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay = False):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout,AI=True)
        self.is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board:chessboard, epsilon=1e-3, return_prob=0):
        sensible_moves = board.possible_move
        # the pi vector returned by MCTS as in the alphaGo Zero paper
        move_probs = np.zeros(64)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move(board, epsilon)
            move_probs[list(acts)] = probs
            if self.is_selfplay:
                # add Dirichlet Noise for exploration (needed for
                # self-play training)
                move = np.random.choice(
                    acts,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                # update the root node and reuse the search tree
                self.mcts.update_with_move(move)
            else:
                # with the epsilon=1e-3, it will choose the move with the highest prob
                move = np.random.choice(acts, p=probs)
                # reset the root node
                self.mcts.update_with_move(-1)

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)