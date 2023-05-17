import threading, gym, random, time

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
            mv = self.random_move()
            #mv = self.choose_next_move()
            if mv != None:
                #time.sleep(0.1)
                self.cb.step(mv,self.color)


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