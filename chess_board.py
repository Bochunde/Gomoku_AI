
import numpy as np


#8x8 chessboard
from agent import agent

class chessboard():
    #chessboard class should define the chessboard state
    #check if game end
    #taking 2 agent as black/white
    # o represents black and x represents white


    def __init__(self):
        self.turn ='Black'

        #initialize chessboard
        self.chessboard = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        #initialize agent
        self.agentBlack = agent()
        self.agentBlack.chess_color='black'

        self.agentWhite = agent()
        self.agentWhite.chess_color='white'

    #action takes agent and action as input
    def action(self,agent:agent,action:tuple):
        if agent.check_action_valid(action):
            if agent.chess_color == 'black':
                #update chessboard
                self.chessboard[action] = 'o' 
                self.agentBlack.chessboard = self.chessboard
                self.agentWhite.chessboard = self.chessboard
                #switch turn
                self.turn = 'white'

            elif agent.chess_color =='white':
                #update chessboard
                self.chessboard[action] = 'x'
                self.agentBlack.chessboard = self.chessboard
                self.agentWhite.chessboard = self.chessboard
                #switch turn
                self.turn = 'black'
        return


    def render(self):
        print(self.turn+' turn')
        self.display_board(self.chessboard)
        if self.check_win():
            print(self.turn + ' wins!')
    def display_board(self):
        border = " | " + " | ".join(str(i) for i in range(1, len(self.chessboard)+1)) + " |"
        print(border)
        for i in range(len(self.chessboard)):
            row = self.chessboard[i]
            row_str = " | ".join(str(s) for s in row)
            print(f"{i+1}| {row_str} |")
        print(border)

    #check_win should run after each time agent takes action
    def check_win(self):
        #check rows for win
        for row in self.chessboard:
            for i in range(len(row)-4):
                if row[i:i+5] == ['o', 'o', 'o', 'o', 'o']:
                    return True
                elif row[i:i+5] == ['x', 'x', 'x', 'x', 'x']:
                    return True
                    
        # Check columns for win
        for j in range(len(self.chessboard)):
            for i in range(len(self.chessboard)-4):
                if [self.chessboard[i+k][j] for k in range(5)] == ['o', 'o', 'o', 'o', 'o']:
                    return True
                elif [self.chessboard[i+k][j] for k in range(5)] == ['x', 'x', 'x', 'x', 'x']:
                    return True
                    
        # Check diagonals for win
        for i in range(len(self.chessboard)-4):
            for j in range(len(self.chessboard)-4):
                if [self.chessboard[i+k][j+k] for k in range(5)] == ['o', 'o', 'o', 'o', 'o']:
                    return True
                elif [self.chessboard[i+k][j+k] for k in range(5)] == ['x', 'x', 'x', 'x', 'x']:
                    return True
                    
                if [self.chessboard[i+k][j+4-k] for k in range(5)] == ['o', 'o', 'o', 'o', 'o']:
                    return True
                elif [self.chessboardard[i+k][j+4-k] for k in range(5)] == ['x', 'x', 'x', 'x', 'x']:
                    return True

        return False
        