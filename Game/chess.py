import time
import random
import threading as td
import multiprocessing as mp

from pieces import pieces_table
from ReiforcementLearning.RLplayer import RLPlayer
from chessboard import Chessboard
from cli_display import print_board

TIME_OUT = 5

class Game:

    def __init__(self, board: list[int] = None, cooldown: int = 0):
        
        if board is None: # * default board
            board = [3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
                     0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,
                     3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
                    ]
        self.cb = Chessboard(
            board,                      # set board
            [int(time.time()) - cooldown - 1] * 64, # set current timestamps
            cooldown                    # set cooldown
        )
        
        self.stop_e = td.Event()
        # Playing as RL
        self.player_1 = RLPlayer(self.cb, 1, self.stop_e)
        # Playing as StockFish
        self.player_2 = StockFishPlayer(self.cb, 2, self.stop_e)
    
    def play(self,verbatim :bool = False ) -> list[tuple[dict[str, int], int]]:
        
        start_time = int(time.time())
        curr_time = int(time.time())
        
        self.player_1.start()
        self.player_2.start()
        
        while ((1+8 in self.cb.board) and (1+16 in self.cb.board)) and (start_time + TIME_OUT > curr_time):
            curr_time = int(time.time())
            if verbatim: print_board(self.cb.board, 8)
            time.sleep(0.1)

        self.stop_e.set()
        
        self.player_1.join()
        self.player_2.join()
        
        #print(f" player 1 fitness {self.player_1.fitness(self.cb.board)} player2 fitness {self.player_2.fitness(self.cb.board)}")

        return 

    def win_condition(self):
        # temporary
        if 1+16 not in self.cb.board: return -1
        if 1+8  not in self.cb.board: return  1
        return 0