import tensorflow as tf
from tensorflow import keras
import logging
import numpy as np

logging.getLogger('tensorflow').setLevel(logging.FATAL)
# CONSTANTS

# discount factor for the reward: [0.9, 0.99]


class NeuralNetwork():

    def __init__(self) -> None:

        # Create a Sequential model and add a Dense layer as the first layer.
        model = keras.models.Sequential()
        model.add(keras.layers.InputLayer(input_shape=(64)))
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dense(32, activation='relu'))
        model.add(keras.layers.Dense(1, activation='relu'))

        model.compile(optimizer='adam',
                      loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        # print(model.summary())
        # print('[INPUT_SHAPE]', model.input_shape)

        self.model = model

    def update(self, x: list[list[int]], y: list[float]):
        """This method given a certain board history and a winner updates the NN

        Args:
            boardHistory (list[tuple[list[int],int]]): List with tuple, where the tuples are (board, current player)
            winner (int): who won the game represented as a int, 1 being white 2 being black
        """

        self.model.fit(x, y, verbose=0)

    def predict(self, board: list[int]) -> float:
        """Given a certain board state, and a group of actions, predict which one is the best

        Args:
            board (list[int]): current board
        """
        arr = np.array(board).reshape(1, -1)

        return self.model.predict(arr, verbose=0)
