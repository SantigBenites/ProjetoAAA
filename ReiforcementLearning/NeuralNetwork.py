import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential

class NeuralNetwork(tf.keras.Model):

    def __init__(self) -> None:
        
        conv_depth = 4
        self.model = Sequential()
        model = self.model

        model.add(layers.Input(shape=(14, 8, 8)))
        for _ in range(conv_depth):
            model.add(layers.Conv2D(kernel_size=3,padding='same', activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, 'relu'))
        model.add(layers.Dense(1, 'sigmoid'))

        model.compile(optimizer='adam', 
              loss=tf.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


    def update(self,boardHistory:list[tuple[list[int],int]], winner:int):
        """This method given a certain board history and a winner updates the NN

        Args:
            boardHistory (list[tuple[list[int],int]]): List with tuple, where the tuples are (board, current player)
            winner (int): who won the game represented as a int, 1 being white 2 being black
        """
        
        x, y = [], [] 
        for board, player in boardHistory:
            x.append(board)
            y.append(player)
        self.model.fit(x,y)


    def predict(self,board:list[int],actions:list[tuple[int,int]]):
        """Given a certain board state, and a group of actions, predict which one is the best

        Args:
            board (list[int]): current board
            actions (list[tuple[int,int]]): list of possible actions
        """

        pass