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

if __name__ == "__main__":
    # Neural Networks
    black_network = NeuralNetwork()
    if os.path.isdir("model/black_model"):
        black_network.model = tf.keras.models.load_model(
            'model/black_model')  # type: ignore

    white_network = NeuralNetwork()
    if os.path.isdir("model/white_model"):
        white_network.model = tf.keras.models.load_model(
            'model/white_model')  # type: ignore

    def task(player_def_1: PlayerDef, player_def_2: PlayerDef, stop_e: td.Event):
        g = Game(player_def_1,
                 player_def_2,
                 Chessboard(config.base_board.copy(), config.cooldown))
        return g.play(verbatim=config.verbose)
