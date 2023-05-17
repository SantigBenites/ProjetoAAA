import tensorflow as tf
import threading as td
from Game.chessboard import Chessboard
from Game.chess import Game
from ReinforcementLearning.RLplayer import RLPlayer
from StockFish.StockFishplayer import StockFishPlayer
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
import time
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Game vars
board = [3+8, 5+8, 4+8, 2+8, 1+8, 4+8, 5+8, 3+8,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         3+16, 5+16, 4+16, 2+16, 1+16, 4+16, 5+16, 3+16
         ]
cooldown = 0.1

# End event
stop_e = td.Event()

# Neural Network
black_network = NeuralNetwork()
if os.path.isdir("model/black_model"):
    black_network.model = tf.keras.models.load_model('model/black_model') # type: ignore

white_network = NeuralNetwork()
if os.path.isdir("model/white_model"):
    white_network.model = tf.keras.models.load_model('model/white_model') # type: ignore

MAX_EPISODES = 1

for episode_num in range(MAX_EPISODES):

    print(f"Starting game {episode_num}")
    # Board
    cb = Chessboard(board.copy(), cooldown)

    # Players
    p1 = RLPlayer(cb, 1, stop_e, black_network)
    p2 = StockFishPlayer(cb, 2, stop_e)

    # Game
    chess = Game(p1, p2, cb, stop_e)

    white_x, white_y, black_x, black_y = chess.play(verbatim=False)

    print(f"Game number {episode_num} was won by player {chess.winner}")
    stop_e.clear()
    p1.join()
    p2.join()

    white_network.update(white_x, white_y)
    black_network.update(black_x, black_y)



white_network.model.save('model/white_model')
black_network.model.save('model/black_model')