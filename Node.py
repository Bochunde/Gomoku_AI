import numpy as np
class Node(object):
    def __init__(self,parent,prior):
        self.parent = parent
        self.children = {}  # action->node
        self.n_visits = 0
        self.Q = 0
        self.P = prior
    
    def expand(self, action_priors:list(tuple)):
        for action, prior in action_priors:
            if action not in self.children:
                self.children[action]=Node(self,prior)

    def select(self,epsilon:int)->tuple:
        maxpair = max(self.children.items(), key=lambda x: x[1].get_value(epsilon))
        return maxpair
    
    def node_value(self,epsilon)->float:
        update = (epsilon * self.P * np.sqrt(self.parent.n_visits)
                  /(1+self.n_visits))
        return self.Q + update
    
    def update(self,child_value:float):
        if self.parent:
            self.parent.update(-child_value)
        self.n_visits += 1
        self.Q += (child_value-self.Q) / self.n_visits
    
    def is_root(self):
        if self.parent:
            return False
        else:
            return True
        
    def is_bottom(self):
        return self.children =={}

