from multiprocessing import set_start_method

import os
import json
import operator
import random
import tensorflow as tf

import matplotlib.pyplot as plt
from Game.chess import Game
from multiprocessing import Pool
from lib.constants import config
from ReinforcementLearning.NeuralNetwork import NeuralNetwork
from lib.typedef import PlayerDef, RlPlayerConfig, GAPlayerConfig, SFPlayerConfig

NUMBER_OF_GAMES = 5

white_network = NeuralNetwork()
if os.path.isdir("../model/white_model"):
    white_network.model = tf.keras.models.load_model('../model/white_model')  # type: ignore

w_mod = tf.keras.models.clone_model(white_network.model)
w_mod.set_weights(white_network.model.get_weights())
w_net = NeuralNetwork(model=w_mod)

black_network = NeuralNetwork()
if os.path.isdir("model/black_model"):
    black_network.model = tf.keras.models.load_model(
        'model/black_model')  # type: ignore

b_mod = tf.keras.models.clone_model(black_network.model)
b_mod.set_weights(black_network.model.get_weights())
b_net = NeuralNetwork(model=b_mod)


Player1 = PlayerDef("RL", RlPlayerConfig(1, w_net))
Player2 = PlayerDef("RL", RlPlayerConfig(2, b_net))

winner = {"P1Wins" : 0,
          "P2Wins" : 0
          }

tournamet = True
import time

if tournamet:

    for x in range(NUMBER_OF_GAMES):

        g = Game(Player1, Player2)
        result = g.play(True)
        if random.randint(0,1) > 0.5:
            print(f"{Player1.type} vs {Player2.type} with win of RL")
        else:
            print(f"{Player1.type} vs {Player2.type} with win of RL")
        time.sleep(0.1)
else:
    g = Game(Player1, Player2)
    result = g.play(True)
