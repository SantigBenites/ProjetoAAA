import os
import tensorflow as tf
import threading as td
import multiprocessing as mp

from Game.chess import Game
from Game.chessboard import Chessboard
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from lib.typedef import PlayerDef, RlPlayerConfig, GAPlayerConfig, SFPlayerConfig

# move all constants to this file
from lib.constants import config

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# End event
# TODO review this
#! this should not one event for every game
stop_e = td.Event()

# Neural Networks
black_network = NeuralNetwork()
if os.path.isdir("model/black_model"):
    black_network.model = tf.keras.models.load_model(
        'model/black_model')  # type: ignore

white_network = NeuralNetwork()
if os.path.isdir("model/white_model"):
    white_network.model = tf.keras.models.load_model(
        'model/white_model')  # type: ignore


for episode_num in range(config.max_episodes):

    print(f"Starting game {episode_num}")
    # Board
    cb = Chessboard(config.base_board.copy(), config.cooldown)

    # Players
    p1_def = PlayerDef("RL", RlPlayerConfig(cb, 1, stop_e, white_network))
    p2_def = PlayerDef("SF", SFPlayerConfig(cb, 2, stop_e))

    # Game
    chess = Game(p1_def, p2_def, cb, stop_e)

    white_x, white_y, black_x, black_y = chess.play(verbatim=False)

    print(f"Game number {episode_num} was won by player {chess.winner}")
    stop_e.clear()

    white_network.update(white_x, white_y)
    black_network.update(black_x, black_y)


white_network.model.save('model/white_model')
black_network.model.save('model/black_model')
