import time
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from ReinforcementLearning.RLplayer import RLPlayer
from Game.chess import Game
from Game.chessboard import Chessboard
import threading as td

# Game vars
board =[3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
        ]
cooldown = 0.01

# End event
stop_e = td.Event()

# Board
cb = Chessboard(board,cooldown * 64,cooldown)

# Neural Network
network = NeuralNetwork()

# Players
p1 = RLPlayer(cb, 1, stop_e,network)
p2 = RLPlayer(cb, 2, stop_e,network)

# Game
chess = Game(p1,p2,cb,stop_e)


chess.play(verbatim=False)