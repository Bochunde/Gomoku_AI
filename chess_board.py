import numpy as np
class chessboard():
    #chessboard class should define the chessboard state
    #check if game end
    #taking 2 agent as black/white


    def __init__(self):
        
        self.players = [1,2]
        #self.curr_agent = 1 
        self.last_move = -1
        #initialize chessboard
        self.states = {}
        self.chessboard = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    def init_board(self, start_player=0):
        self.current_player = self.players[start_player]  # start player
        # keep available moves in a list
        self.possible_move = list(range(64))
        self.states = {}
        self.last_move = -1

    def current_state(self):
            """return the board state from the perspective of the current player.
            state shape: 4*width*height
            """

            square_state = np.zeros((4, 8, 8))
            if self.states:
                moves, players = np.array(list(zip(*self.states.items())))
                move_curr = moves[players == self.current_player]
                move_oppo = moves[players != self.current_player]
                square_state[0][move_curr // 8,
                                move_curr % 8] = 1.0
                square_state[1][move_oppo // 8,
                                move_oppo % 8] = 1.0
                # indicate the last move location
                square_state[2][self.last_move // 8,
                                self.last_move % 8] = 1.0
            if len(self.states) % 2 == 0:
                square_state[3][:, :] = 1.0  # indicate the colour to play
            return square_state[:, ::-1, :]


    #action takes agent and action as input
    def action(self,action:int):
        #action: (x,y) in chessboard
        self.states[action] = self.current_player
        
        self.possible_move.remove(action)
        h = action //8
        w = action % 8
        self.chessboard[h][w] = 'X' if self.current_player ==1 else 'O'
        #update current agant
        self.current_player = (
            self.players[0] if self.current_player == self.players[1]
            else self.players[1]
        )
        self.last_move = action

    def render(self)->None:
        curr_player = 'Player2' if self.current_player==2 else 'Player1'
        print(curr_player+' turn')         
        self.display_board()
        end,winner = self.game_end()
        if end:
            if winner ==1:
                print('Player1 wins!')
                return
            elif winner==2:
                print('Player2 wins!')
                return
            else:
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
    def check_win(self):
        #check rows for win
        for row in self.chessboard:
            for i in range(len(row)-4):
                if row[i:i+5] == ['O', 'O', 'O', 'O', 'O']:
                    return (True,2)
                elif row[i:i+5] == ['X', 'X', 'X', 'X', 'X']:
                    return (True,1)
                    
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
                elif [self.chessboard[i+k][j+4-k] for k in range(5)] == ['X', 'X', 'X', 'X', 'X']:
                    return True,1

        return False,-1
    
    def has_a_winner(self):
        width = 8
        height = 8
        states = self.states
        n = 5

        moved = list(set(range(width * height)) - set(self.possible_move))
        if len(moved) < 5 *2-1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1
    
    def game_end(self):
        end,winner = self.has_a_winner()
        if end:
            return end,winner
        elif len(self.possible_move)==0:#end is false and board is full
            return True,-1
        else:
            return False,-1
    