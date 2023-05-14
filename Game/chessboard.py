from attrs import define, field
from Game.moveGeneration import possible_moves
from copy import deepcopy
from Game.moveGeneration import distance_to_edge
import time, gym,itertools


class Chessboard(gym.Env):

    #self.board: list[int] = field(factory=list[int])
    #self.timestamps: list[int] = field(factory=list[int])
    #self.cooldown: int = 0


    def __init__(self, board: list[int], cooldown: int, render_mode=None):

        distance_to_edge()
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

    def step(self, action: tuple[int,int], player:int) -> None:

        current_index, final_index = action
        self.move(current_index, final_index)
        
        reward = self._reward(player)
        observation = self._observation()
        done = self.win_condition()

        return observation, reward, done, None
    
    def move(self, current_index: int, final_index: int):
        self.board[final_index] = self.board[current_index]
        self.board[current_index] = 0
        
        self.timestamps[final_index] = int(time.time())

    def destroyEnemyKing(self,player:int):

        if player == 1 :
            # 1+16
            self.board[self.board.index(1+16)] = 0
        else:
            # 1+8
            print("removed 1+8")
            self.board[self.board.index(1+8)] = 0

        return self._observation()

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
        my_pieces = list(filter(lambda index: (self.board[index] >> 3 == color), range(0, 64)))
        for piece in my_pieces:
            legal_moves.append(self.valid_moves(piece))
            
        return list(itertools.chain(*legal_moves))
    
    def valid_moves(self, index: int) -> list[int]:
        
        current_time = int(time.time())
        
        if current_time - self.timestamps[index] >= self.cooldown:
            pm = possible_moves(self.board, index)
            return zip([index]*len(pm),pm)
        return []
    
    def pieceOnCooldown(self,index:int) -> bool:

        current_time = int(time.time())
        return True if current_time - self.timestamps[index] >= self.cooldown else False

    # Gym vars

    def _reward(self, player):
        if player == 1 :
            if 1+16 not in self.board: return  1
            if 1+8  not in self.board: return -1
        else:
            if 1+16 not in self.board: return -1
            if 1+8  not in self.board: return  1
        return 0


    def _observation(self):

        return self.board
    

    def win_condition(self):

        return True if 1+16 not in self.board or 1+8  not in self.board else False