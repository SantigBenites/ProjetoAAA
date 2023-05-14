from attrs import define, field
from Game.moveGeneration import possible_moves
from copy import deepcopy
import time, gym


class Chessboard(gym.Env):

    #self.board: list[int] = field(factory=list[int])
    #self.timestamps: list[int] = field(factory=list[int])
    #self.cooldown: int = 0


    def __init__(self, board: list[int], cooldown: int, render_mode=None):

        # Original
        self.originalboard = board 
        self.cooldown = cooldown
        # In use
        self.board = board
        self.timestamps = [int(time.time()) - self.cooldown - 1] * 64

    # Step()
    # Updates an environment with actions returning the next agent observation, the reward for taking that actions, 
    # if the environment has terminated or truncated due to the latest action and information from the environment 
    # about the step, i.e. metrics, debug info.

    def step(self, action: tuple[int,int]) -> None:

        current_index, final_index = action
        self.move(current_index, final_index)
        
        reward = self._reward()
        observation = self._observation()
        done = self.game.win_condition

        return observation, reward, done, None
    
    def move(self, current_index: int, final_index: int):
        self.board[final_index] = self.board[current_index]
        self.board[current_index] = 0
        
        self.timestamps[final_index] = int(time.time())

    # Reset()
    # Resets the environment to an initial state, required before calling step. 
    # Returns the first agent observation for an episode and information, i.e. metrics, debug info.

    def reset(self):
        self.board = deepcopy(self.originalBoard)
        self.timestamps = [int(time.time()) - self.cooldown - 1] * 64


    # Render()
    # Renders the environments to help visualise what the agent see, 
    # examples modes are “human”, “rgb_array”, “ansi” for text.

    def reset(self):

        return
    
    # Close()
    # Closes the environment, important when external software is used.

    def close(self):
        
        return 

    def legal_moves(self,color) -> list[(int,int)]:
        """Legal moves for the current player."""

        legal_moves:list(tuple[int,int]) = []
        my_pieces = list(filter(lambda index: (self.cb.board[index] >> 3 == color), range(0, 64)))
        for piece in my_pieces:
            legal_moves.append(self.valid_moves(piece))
            
        return legal_moves
    
    def valid_moves(self, index: int) -> list[int]:
        
        current_time = int(time.time())
        
        if current_time - self.cb.timestamps[index] >= self.cb.cooldown:
            pm = possible_moves(self.cb.board, index)
            return zip([index]*len(pm),pm)
        return []