import numpy as np
from Node import Node
from chess_board import chessboard
import copy
def softmax(x):
    probs = np.exp(x - np.max(x))
    probs = probs / np.sum(probs)
    return probs
class MCTS(object):
    def __init__(self, policy_value_fn, epsilon=5, n_step=10000,AI=False):
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
        self.AI = AI
    def play(self, chessboard:chessboard):
        "playout"
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self.root
        while(1):
            if node.is_leaf():
                break
            # Greedily select next move.
            action, node = node.select(self.epsilon)
            chessboard.action(action)
        
        action_probs, leaf_value = self.policy(chessboard)
        # Check for end of game
        end, winner = chessboard.game_end()

        if self.AI==False:
            if not end:
                node.expand(action_probs)
            # Evaluate the leaf node by random rollout
            leaf_value = self.evaluate_rollout(chessboard)
            node.update(-leaf_value)
        else:
            leaf_value = leaf_value.cpu().numpy()
            if end==False:
                node.expand(action_probs)
            else:
                # for end state，return the "true" leaf_value

                if winner == -1:  # tie
                    leaf_value = 0.0
                else:
                    leaf_value = (
                        1.0 if winner == chessboard.current_player else -1.0
                    ) 
        node.update_recursive(-leaf_value)

    def rollout_policy_fn(board:chessboard):
        """a coarse, fast version of policy_fn used in the rollout phase."""
        # rollout randomly
        action_probs = np.random.rand(len(board.availables))
        return zip(board.availables, action_probs)
    
    def evaluate_rollout(self, chessboard:chessboard, limit=1000):
        """Use the rollout policy to play until the end of the game,
        returning +1 if the current player wins, -1 if the opponent wins,
        and 0 if it is a tie.
        """
        player = chessboard.current_player
        for i in range(limit):
            end, winner = chessboard.game_end()
            if end:
                break
            action_probs = self.rollout_policy_fn(chessboard)
            action = max(action_probs, key=lambda x: x[1])[0]
            #max_action = max(action_probs, key=itemgetter(1))[0]
            chessboard.action(action)
        else:
            # If no break from the loop, issue a warning.
            print("WARNING: rollout reached move limit")
        if winner == -1:  # tie
            return 0
        elif winner==player:
            return 1
        else:
            return -1

    def get_move(self, chessboard:chessboard,epsilon):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state

        Return: the selected action
        """
        print(len(chessboard.possible_move))
        for n in range(self.n_step):
            chessboard_copy = copy.deepcopy(chessboard)
            self.play(chessboard_copy)
        
        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node.n_visits) for act, node in self.root.children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/epsilon * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):
        """Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            print(last_move)
            print('go back to root')
            self.root = Node(None, 1.0)

    def __str__(self):
        return "MCTS"


