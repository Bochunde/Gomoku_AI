from agent import agent
import numpy as np
class chessboard():
    #chessboard class should define the chessboard state
    #check if game end
    #taking 2 agent as black/white
    # o represents black and x represents white


    def __init__(self):
        self.possible_move = np.ones((8,8))
        self.playerX = agent(1)
        self.playerO = agent(2)
        self.curr_agent = self.playerX
        self.last_move = None
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



    #action takes agent and action as input
    def action(self,action:tuple):
        #action: (x,y) in chessboard
        self.chessboard[action] = 'X' if self.curr_agent ==self.playerX else 'O'
        self.possible_move[action]=-1
        self.curr_agent = self.playerX if self.curr_agent==self.playerO else self.playerO
        self.last_move = action

##need to modify
    def render(self)->None:
        curr_player = 'Player2' if self.curr_agent.order==1 else 'Player1'
        print(curr_player+' turn')         
        self.display_board(self.chessboard)
        end,winner = self.check_win()
        if end:
            if winner ==1:
                print('Player1 wins!')
                return
            else:
                print('Player2 wins!')
                return
        elif np.all(self.possible_move==-1):
            print('tie')
            return
    def display_board(self):
        border = " | " + " | ".join(str(i) for i in range(1, len(self.chessboard)+1)) + " |"
        print(border)
        for i in range(len(self.chessboard)):
            row = self.chessboard[i]
            row_str = " | ".join(str(s) for s in row)
            print(f"{i+1}| {row_str} |")
        print(border)

    #check_win should run after each time agent takes action
    def check_win(self)->tuple(bool ,int):
        #check rows for win
        for row in self.chessboard:
            for i in range(len(row)-4):
                if row[i:i+5] == ['O', 'O', 'O', 'O', 'O']:
                    return True,2
                elif row[i:i+5] == ['X', 'X', 'X', 'X', 'X']:
                    return True,1
                    
        # Check columns for win
        for j in range(len(self.chessboard)):
            for i in range(len(self.chessboard)-4):
                if [self.chessboard[i+k][j] for k in range(5)] == ['O', 'O', 'O', 'O', 'O']:
                    return True,2
                elif [self.chessboard[i+k][j] for k in range(5)] == ['X', 'X', 'X', 'X', 'X']:
                    return True,1
                    
        # Check diagonals for win
        for i in range(len(self.chessboard)-4):
            for j in range(len(self.chessboard)-4):
                if [self.chessboard[i+k][j+k] for k in range(5)] == ['O', 'O', 'O', 'O', 'O']:
                    return True,2
                elif [self.chessboard[i+k][j+k] for k in range(5)] == ['X', 'X', 'X', 'X', 'X']:
                    return True,1
                    
                if [self.chessboard[i+k][j+4-k] for k in range(5)] == ['O', 'O', 'O', 'O', 'O']:
                    return True,2
                elif [self.chessboardard[i+k][j+4-k] for k in range(5)] == ['X', 'X', 'X', 'X', 'X']:
                    return True,1

        return False
    