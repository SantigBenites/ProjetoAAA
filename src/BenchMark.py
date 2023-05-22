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

NUMBER_OF_GAMES = 100

white_network = NeuralNetwork()
if os.path.isdir("../model/white_model"):
    white_network.model = tf.keras.models.load_model('../model/white_model')  # type: ignore

w_mod = tf.keras.models.clone_model(white_network.model)
w_mod.set_weights(white_network.model.get_weights())
w_net = NeuralNetwork(model=w_mod)

Player1 = PlayerDef("RL", RlPlayerConfig(1, w_net))
Player2 = PlayerDef("SF", SFPlayerConfig(2))

winner = {"P1Wins" : 0,
          "P2Wins" : 0
          }

for x in range(NUMBER_OF_GAMES):

    g = Game(Player1, Player2)
    result = g.play()

    if result.winner == 1:
        winner["P1Wins"] += 1
    elif result.winner == 2:
        winner["P2Wins"] += 1
    else:
        pass


courses = ["RL","SF"]
values = [winner["P1Wins"], winner["P2Wins"]]

plt.bar(courses, values, color ='maroon',width = 0.4)

plt.title("Games won by each player")
plt.show()
