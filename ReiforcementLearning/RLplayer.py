import threading, gym, random, time

from Game.pieces import pieces_table
from Game.chessboard import Chessboard
from Game.cli_display import board_string

class RLPlayer(threading.Thread):

    def __init__(self, c_board: Chessboard, color: int, stop: threading.Event, env) -> None:
        threading.Thread.__init__(self, daemon=True) 
        self.cb = c_board
        self.stop = stop
        self.color = color
        
    def run(self) -> None:
        # we will need to implement the algorithm here
        while not self.stop.is_set():
            #self.random_move()
            mv = self.choose_next_move()
            time.sleep(0.1)
            self.cb.step(mv)


    def _observation(self) -> Chessboard:
        """Returns the current board position."""
        return self._board.copy()
    

    def _reward(self) -> float:
        """Returns the reward for the most recent move."""

        return self.game.win_condition()
