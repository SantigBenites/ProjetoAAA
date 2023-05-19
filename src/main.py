from multiprocessing import set_start_method

import os
import operator
import tensorflow as tf


from functools import reduce
from Game.chess import Game
from multiprocessing import Pool
from lib.constants import config
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from lib.typedef import PlayerDef, RlPlayerConfig, GAPlayerConfig, SFPlayerConfig

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
tf.keras.utils.disable_interactive_logging()
tf.get_logger().setLevel("WARNING")


def get_player_pairs_init(pop_size: int, white_net: NeuralNetwork, black_net: NeuralNetwork):
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


def get_player_pairs_train(pop_size: int, white_net: NeuralNetwork, black_net: NeuralNetwork):
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
                        PlayerDef("RL", RlPlayerConfig(2, b_net))))
        else:
            res.append((PlayerDef("RL", RlPlayerConfig(1, w_net)),
                        PlayerDef("RL", RlPlayerConfig(2, b_net))))
    return res


dataFrameTrain = {"episode": [],
                  "duration": [],
                  "step_num": [],
                  "GamesWonByBlack": 0,
                  "GameWonByWhite": 0}


def task(player_def_1: PlayerDef, player_def_2: PlayerDef):
    g = Game(player_def_1, player_def_2)
    return g.play()


def task_train(player_def_1: PlayerDef, player_def_2: PlayerDef):
    g = Game(player_def_1, player_def_2)
    return g.play()


if __name__ == "__main__":
    set_start_method("spawn")  # * talk about this in the report
    # Neural Networks
    black_network = NeuralNetwork()
    if os.path.isdir("model/black_model"):
        black_network.model = tf.keras.models.load_model(
            'model/black_model')  # type: ignore

    white_network = NeuralNetwork()
    if os.path.isdir("model/white_model"):
        white_network.model = tf.keras.models.load_model(
            'model/white_model')  # type: ignore

    # Stockfish train episodes
    # for episode_num in range(3):
    #    print('[INFO]', f'Starting episode {episode_num}')
    #
    #    results = []
    #    pairs = get_player_pairs_init(config.pop_size,
    #                                  white_net=white_network,
    #                                  black_net=black_network)
    #
    #    print('[MAIN]: get_pairs', pairs)
    #
    #    with Pool() as pool:
    #        results = pool.starmap(task, pairs)
    #        pool.close()
    #
    #    white_x: list[list[int]] = []
    #    white_y: list[float] = []
    #    black_x: list[list[int]] = []
    #    black_y: list[float] = []
    #    for res in results:
    #        white_x.extend(res.white_x)
    #        white_y.extend(res.white_y)
    #        black_x.extend(res.black_x)
    #        black_y.extend(res.black_y)
    #
    #    for (x, y) in zip(white_x, white_y):
    #        white_network.update(x, y)
    #
    #    for (x, y) in zip(black_x, black_y):
    #        black_network.update(x, y)

    # RL Train Episodes
    for episode_num in range(200):
        print('[INFO]', f'Starting episode {episode_num}')

        results = []
        pairs = get_player_pairs_train(config.pop_size,
                                       white_net=white_network,
                                       black_net=black_network)

        # print('[MAIN]: get_pairs', pairs)

        with Pool() as pool:
            results = pool.starmap(task, pairs)
            pool.close()

        white_x: list[list[int]] = []
        white_y: list[float] = []
        black_x: list[list[int]] = []
        black_y: list[float] = []
        for res in results:
            white_x.extend(res.white_x)
            white_y.extend(res.white_y)
            black_x.extend(res.black_x)
            black_y.extend(res.black_y)

            dataFrameTrain["episode"].append(episode_num)
            dataFrameTrain["duration"].append(res.duration)
            dataFrameTrain["step_num"].append(res.moves_num)
            if res.winner == 1:
                dataFrameTrain["GameWonByWhite"] += 1
            else:
                dataFrameTrain["GamesWonByBlack"] += 1

            print('[INFO]', f'got all results in episode {episode_num}')

        white_network.update(white_x, white_y)

        black_network.update(black_x, black_y)
        white_network.model.save('model/white_model')
        black_network.model.save('model/black_model')

    import json
    with open('assets/data.txt', 'w') as convert_file:
        convert_file.write(json.dumps(dataFrameTrain))

    white_network.model.save('model/white_model')
    black_network.model.save('model/black_model')
