import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
import logging
import numpy as np


logging.getLogger('tensorflow').setLevel(logging.FATAL)
# CONSTANTS

NN_WIN_REWARD: int = 50  # reward for the winning move
DISCOUNT_FACTOR: float = 0.9  # discount factor for the reward: [0.9, 0.99]


class NeuralNetwork(tf.keras.Model):

    def __init__(self) -> None:
        super().__init__()
        
        # Create a Sequential model and add a Dense layer as the first layer.
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(16))
        model.add(tf.keras.layers.Dense(1))
        

        model.compile(optimizer='adam',
                      loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        
        self.model = model

    def update(self, boardHistory: list[tuple[list[int], int]], winner: int):
        """This method given a certain board history and a winner updates the NN

        Args:
            boardHistory (list[tuple[list[int],int]]): List with tuple, where the tuples are (board, current player)
            winner (int): who won the game represented as a int, 1 being white 2 being black
        """

        x, y = [], []
        boardHistory.reverse()
        reward = NN_WIN_REWARD
        for board, player in boardHistory:
            if player == winner and reward > 0:
                x.append(board)
                y.append(reward)
                reward *= DISCOUNT_FACTOR  # the first reward should be the full reward

            # if reward < 0:
            #    break

        self.model.fit(x, y)

    def predict(self, board: list[int]) -> float:
        """Given a certain board state, and a group of actions, predict which one is the best

        Args:
            board (list[int]): current board
        """
        arr = np.array(board)
        print(arr.shape)
        return self.model.predict(arr)
