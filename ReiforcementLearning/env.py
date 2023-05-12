import numpy as np
import gym, time
from ProjetoVDA.chess import Game
from ProjetoVDA.chessboard import Chessboard
from ProjetoVDA.moveGeneration import possible_moves
from ProjetoVDA.cli_display import board_string


class ChessEnv(gym.Env):



    def __init__(self) -> None:
        
        self.game = Game(cooldown=4)
        self.cb = self.game.cb
        
        
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

        # Restarts Chess Board
        self.game = Game(cooldown=4)
        self.cb = self.game.cb

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