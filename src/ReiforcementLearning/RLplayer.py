import threading
import random
import time

from Game.pieces import pieces_table
from Game.chessboard import Chessboard
from Game.cli_display import board_string


class RLPlayer(threading.Thread):

    def __init__(self, c_board: Chessboard, color: int, stop: threading.Event, NeuralNetwork) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.cb = c_board
        self.stop = stop
        self.color = color

    def run(self) -> None:
        # we will need to implement the algorithm here
        while not self.stop.is_set():

            # TODO play function
            # this "5" is something we can tune
            for i in range(5):
                # see the return of the moves ahead:
                # get a list of possible moves
                # get their value from the neural network
                # choose the best one
                # repeat until we are 5 layers deep
                # then do the move that got to that best move
                pass

            # TODO about the neural network:
            # this nn will receive a board and return its value
            # it will be trained with the experience of the games

            mv = self.random_move()
            # mv = self.choose_next_move()
            if mv != None:
                # time.sleep(0.1)
                self.cb.step(mv, self.color)

    def _observation(self) -> Chessboard:
        """Returns the current board position."""
        return self._board.copy()

    def _reward(self) -> float:
        """Returns the reward for the most recent move."""

        return self.game.win_condition()

    def random_move(self):
        moves = self.cb.legal_moves(self.color)
        if moves:
            return random.choice(moves)
        else:
            return None
