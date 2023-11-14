from play import Game
from chess_board import chessboard
from MCTS import MCTS 
from Node import Node
from agent_AI import agent_AI
from agent import agent
from agent_human import agent_human
import os
from policy_network import PolicyValueNet
def play_demo():
    return

if __name__=='__main__':
    board = chessboard()
    game = Game(board)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)    
    policy_file = 'trained_policy/best_policy_12.model' 
    p_fc = PolicyValueNet(policy_file).policy_value_fn
    p1 = agent_human()
    p2 = agent()
    game.start_play(p1,p2,start_player=0,is_shown=True)