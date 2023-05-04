import numpy as np
class Node(object):
    def __init__(self,parent,prior):
        self.parent = parent
        self.children = {}  # action->node
        self.n_visits = 0
        self.Q = 0
        self.P = prior
    
    def expand(self, action_priors):
        for action, prior in action_priors:
            if action not in self.children:
                self.children[action]=Node(self,prior)

    def select(self,epsilon:int)->tuple:
        #return int and Node
        maxpair = max(self.children.items(), key=lambda x: x[1].node_value(epsilon))
        return maxpair
    
    def node_value(self,epsilon)->float:
        update = (epsilon * self.P * np.sqrt(self.parent.n_visits)
                  /(1+self.n_visits))
        return self.Q + update
    
    def update(self,leaf_value:float):
        self.n_visits += 1
        # Update Q, a running average of values for all visits.
        self.Q += 1.0*(leaf_value - self.Q) / self.n_visits

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def is_root(self):
        return self.parent is None
        
    def is_leaf(self):
        return self.children =={}

