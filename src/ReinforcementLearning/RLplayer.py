import threading
import random
import time

from lib.constants import config
from lib.typedef import RlPlayerConfig
from Game.chessboard import Chessboard


class RLPlayer(threading.Thread):

    def __init__(self, config: RlPlayerConfig, c_board: Chessboard, stop: threading.Event) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.cb = c_board
        self.color = config.color
        self.NN = config.NN
        self.stop = stop

    # def __init__(self, c_board: Chessboard, color: int, stop: threading.Event, NN: NeuralNetwork) -> None:
    #    threading.Thread.__init__(self, daemon=True)
    #    self.cb = c_board
    #    self.stop = stop
    #    self.color = color
    #    self.NN = NN

    def run(self) -> None:
        # we will need to implement the algorithm here
        while not self.stop.is_set():

            # TODO about the neural network:
            # this nn will receive a board and return its value
            # it will be trained with the experience of the games

            mv = self.choose_next_move()
            # mv = self.choose_next_move()
            if mv != None:
                # time.sleep(0.1)
                self.cb.step(mv, self.color)

    def choose_next_move(self) -> None | tuple[int, int]:

        current_moves = self.cb.legal_moves(self.color)

        if current_moves == []:
            return None

        rand = random.Random()
        if rand.random() < 0.3:
            return random.choice(current_moves)

        move_values = []
        for move in current_moves:
            pred_board = self.cb.move_sim(move[0], move[1])
            pred_value = self.NN.predict(pred_board)

            move_values.append((move, pred_value))

        if len(move_values) == 0:
            return None
        max_move, max_value = max(move_values, key=lambda x: x[1])

        return max_move

    def random_move(self):
        moves = self.cb.legal_moves(self.color)
        if moves:
            return random.choice(moves)
        else:
            return None
