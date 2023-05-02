import numpy as np
from Node import Node
from AlphaZero_Gomoku.game import Board


class MCTS(object):
    def __init__(self, policy_value_fn, epsilon=5, n_step=10000):
        """
        policy_value_fn: a function that takes in a board state and outputs
            a list of (action, probability) tuples and also a score in [-1, 1]
            (i.e. the expected value of the end game score from the current
            player's perspective) for the current player.
        epsilon: a number in (0, inf) that controls how quickly exploration
            converges to the maximum-value policy. A higher value means
            relying on the prior more.
        """
        self.root = Node(None, 1.0)
        self.policy = policy_value_fn
        self.epsilon = epsilon
        self.n_step = n_step
        
    def play(self, chessboard:Board):
        "playout"
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self.root
        while True:
            if node.is_bottom():
                break
            # Greedily select next move.
            action, node = node.select(self.epsilon)
            chessboard.do_move(action)

        action_probs, _ = self.policy(chessboard)
        # Check for end of game
        end, winner = chessboard.game_end()
        if not end:
            node.expand(action_probs)
        # Evaluate the leaf node by random rollout
        leaf_value = self.evaluate_rollout(chessboard)
        node.update(-leaf_value)

    def rollout_policy_fn(board:Board):
        """a coarse, fast version of policy_fn used in the rollout phase."""
        # rollout randomly
        action_probs = np.random.rand(len(board.availables))
        return zip(board.availables, action_probs)
    
    def evaluate_rollout(self, chessboard:Board, limit=1000):
        """Use the rollout policy to play until the end of the game,
        returning +1 if the current player wins, -1 if the opponent wins,
        and 0 if it is a tie.
        """
        player = chessboard.get_current_player()
        for i in range(limit):
            end, winner = chessboard.game_end()
            if end:
                break
            action_probs = self.rollout_policy_fn(chessboard)
            action = max(action_probs, key=lambda x: x[1])[0]
            #max_action = max(action_probs, key=itemgetter(1))[0]
            chessboard.do_move(action)
        else:
            # If no break from the loop, issue a warning.
            print("WARNING: rollout reached move limit")
        if winner == -1:  # tie
            return 0
        elif winner==player:
            return 1
        else:
            return -1

    def get_move(self, chessboard:Board):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state

        Return: the selected action
        """
        for n in range(self.n_step):
            state_copy = np.array(chessboard)
            self.play(state_copy)
        return max(self.root.children.items(),
                   key=lambda act_node: act_node[1].n_visit)[0]

    def update_with_move(self, last_move):
        """Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            self.root = Node(None, 1.0)

    def __str__(self):
        return "MCTS"


