from play import Game
from chess_board import chessboard
from MCTS import MCTS 
from Node import Node
from agent_AI import agent_AI
from agent import agent
from agent_human import agent_human
import os

def play_demo():
    return

if __name__=='__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)    
    policy_file = 'trained_policy/best_policy.model'