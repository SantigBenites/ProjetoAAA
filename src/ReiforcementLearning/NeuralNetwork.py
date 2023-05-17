import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential

# CONSTANTS

NN_WIN_REWARD: int = 50  # reward for the winning move
DISCOUNT_FACTOR: float = 0.9  # discount factor for the reward: [0.9, 0.99]


class NeuralNetwork(tf.keras.Model):

    def __init__(self) -> None:

        conv_depth = 4
        self.model = Sequential()
        model = self.model

        model.add(layers.Input(shape=(64)))
        for _ in range(conv_depth):
            model.add(layers.Conv2D(filters=3, kernel_size=3,
                      padding='same', activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, 'relu'))
        model.add(layers.Dense(1, 'sigmoid'))

        model.compile(optimizer='adam',
                      loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

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
        return self.model.predict(board)
