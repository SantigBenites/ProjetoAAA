import threading, gym, random

from Game.pieces import pieces_table
from Game.moveGeneration import possible_moves
from Game.chessboard import Chessboard
from Game.cli_display import board_string

import time

class RLPlayer(gym.Env):

    def __init__(self, c_board: Chessboard, color: int, stop: threading.Event) -> None:
        threading.Thread.__init__(self, daemon=True) 
        self.cb = c_board
        self.stop = stop
        self.color = color
        
    def run(self) -> None:
        while not self.stop.is_set():
            #self.random_move()
            mv = self.choose_next_move()
            time.sleep(0.1)
            self.move(mv[0], mv[1])

    def step(self, action: tuple[int,int]) -> tuple[Chessboard, float, bool, None]:
        # Takes input from player and updates the game
        
        current_index, final_index = action
        
        self.cb.board[final_index] = self.cb.board[current_index]
        self.cb.board[current_index] = 0
        
        self.cb.timestamps[final_index] = int(time.time())


        reward = self._reward()
        observation = self._observation()
        done = self.game.win_condition

        return observation, reward, done, None


    def reset(self) -> Chessboard:

        return self._observation()

    def render(self, mode: str = 'unicode') -> str:
        # Shows Chess Board using cli_display
        
        return board_string(self.cb.board, 8)


    def close(self):
        # Closes enviroment


        return

    @property
    def legal_moves(self) -> list[(int,int)]:
        """Legal moves for the current player."""

        legal_moves:list(tuple[int,int]) = []
        my_pieces = list(filter(lambda index: (self.cb.board[index] >> 3 == self.color), range(0, 64)))
        for piece in my_pieces:
            legal_moves.append(self.valid_moves(piece))
            
        return legal_moves
    
    def valid_moves(self, index: int) -> list[int]:
        
        current_time = int(time.time())
        
        if current_time - self.cb.timestamps[index] >= self.cb.cooldown:
            pm = possible_moves(self.cb.board, index)
            return zip([index]*len(pm),pm)
        return []


    def _observation(self) -> Chessboard:
        """Returns the current board position."""
        return self._board.copy()
    

    def _reward(self) -> float:
        """Returns the reward for the most recent move."""

        return self.game.win_condition()
