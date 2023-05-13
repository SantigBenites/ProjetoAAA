import threading, gym, random, time

from Game.pieces import pieces_table
from Game.moveGeneration import possible_moves
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
            self.step(mv)

    def step(self, action: tuple[int,int]) -> tuple[Chessboard, float, bool, None]:
        # Takes input from player and updates the game
        
        current_index, final_index = action
        self.move(current_index, final_index)

        reward = self._reward()
        observation = self._observation()
        done = self.game.win_condition

        return observation, reward, done, None
    
    def move(self, current_index: int, final_index: int):
        self.cb.board[final_index] = self.cb.board[current_index]
        self.cb.board[current_index] = 0
        
        self.cb.timestamps[final_index] = int(time.time())


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
