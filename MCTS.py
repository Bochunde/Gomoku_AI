import math
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0.0
        
    def select_child(self):
        selected_child = None
        best_ucb1 = -1
        
        for child in self.children:
            ucb1 = child.score / child.visits + math.sqrt(2 * math.log(self.visits) / child.visits)
            if ucb1 > best_ucb1:
                selected_child = child
                best_ucb1 = ucb1
                
        return selected_child
        
    def expand(self):
        move = random.choice(self.state.get_legal_moves())
        new_state = self.state.apply_move(move)
        new_child = Node(new_state, parent=self)
        self.children.append(new_child)
        return new_child
    
    def update(self, score):
        self.visits += 1
        self.score += score
        
        if self.parent is not None:
            self.parent.update(score)
        
class MCTS:
    def __init__(self, state):
        self.root = Node(state)
        
    def simulate(self, num_iterations):
        for i in range(num_iterations):
            node = self.root
            
            while not node.state.is_terminal():
                if len(node.children) == 0:
                    node = node.expand()
                    break
                else:
                    node = node.select_child()
            
            score = self.simulate_random_playout(node.state)
            node.update(score)
            
    def simulate_random_playout(self, state):
        while not state.is_terminal():
            move = random.choice(state.get_legal_moves())
            state = state.apply_move(move)
            
        return state.get_score()
    
    def get_best_move(self):
        best_child = max(self.root.children, key=lambda child: child.visits)
        return best_child.state.get_last_move()
