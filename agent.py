import numpy as np

class agent():
    #should have two mode: manually 'human' and train_AI: 'AI'
    #should have different action
    #should have a validation function to check if the input is valid


    def __init__(self) :
        self.chess_color = 'black'
        
        #chessboard need to be updated every valid action end.
        self.chessboard = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        self.mode = ''
        return 

    
    def check_action_valid(self,action:tuple):
        #action should be a tuple
        position =action[0]+action[1]*8
        if self.mode =='AI':
            return True
        else:
            if position < 0 or position > 63 or self.chessboard[action] != ' ':
                return False

        return True

    def action(self,action:tuple):
        go = True
        if self.check_action_valid(action)==False:
            print('The position is invalid')
            go = False
            return go


        #action function returns the wether agent actually take the action
        return go
    

    #take action, should return observation of the chessboard
    def step(self):
        output = 0
        if self.mode=='human':
            output = 1
        elif self.mode== 'AI':
            output = 0
        return
    
