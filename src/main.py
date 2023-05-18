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


def get_player_pairs(pop_size: int, white_net: NeuralNetwork, black_net: NeuralNetwork):
    res: list[tuple[PlayerDef, PlayerDef]] = []
    for i in range(pop_size):

        w_mod = tf.keras.models.clone_model(white_net.model)
        w_mod.set_weights(white_net.model.get_weights())
        w_net = NeuralNetwork(model=w_mod)

        b_mod = tf.keras.models.clone_model(black_net.model)
        b_mod.set_weights(black_net.model.get_weights())
        b_net = NeuralNetwork(model=b_mod)

        if i % 2 == 0:
            res.append((PlayerDef("RL", RlPlayerConfig(1, w_net)),
                        PlayerDef("SF", SFPlayerConfig(2))))
        else:
            res.append((PlayerDef("RL", RlPlayerConfig(2, b_net)),
                        PlayerDef("SF", SFPlayerConfig(1))))
    return res


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

    def task(player_def_1: PlayerDef, player_def_2: PlayerDef):
        g = Game(player_def_1, player_def_2)
        return g.play()

    for episode_num in range(config.max_episodes):
        print('[INFO]', f'Starting episode {episode_num}')

        results = []
        pairs = get_player_pairs(config.pop_size,
                                 white_net=white_network,
                                 black_net=black_network)

        with mp.Pool() as pool:
            results = pool.starmap(task, pairs)
            pool.close()

        white_x, white_y, black_x, black_y = list(map(list, zip(*results)))
        print('[INFO]', f'got all results in episode {episode_num}')

        white_network.update(white_x, white_y)
        black_network.update(black_x, black_y)

    white_network.model.save('model/white_model')
    black_network.model.save('model/black_model')
