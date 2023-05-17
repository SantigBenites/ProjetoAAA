import time
import random
import threading as td
import multiprocessing as mp

from Game.pieces import pieces_table
from ReiforcementLearning.RLplayer import RLPlayer
from StockFish.StockFishplayer import StockFishPlayer
from Game.chessboard import Chessboard
from Game.cli_display import print_board, board_string
from copy import deepcopy

TIME_OUT = 15


class Game:

    def __init__(self, player1, player2, board: Chessboard, stop: td.Event):

        # Board / environment
        self.originalBoard = deepcopy(board)

        # Board
        self.cb = board

        # Events for threads
        self.stop_e = stop

        # Playing as RL
        self.player_1 = player1
        # Playing as StockFish
        self.player_2 = player2

    def play(self, verbatim: bool = False) -> list[tuple[dict[str, int], int]]:

        start_time = int(time.time())
        curr_time = int(time.time())

        self.player_1.start()
        self.player_2.start()

        # and (start_time + TIME_OUT > curr_time):
        while ((1+8 in self.cb.board) and (1+16 in self.cb.board)):
            curr_time = int(time.time())
            if verbatim:
                print_board(self.cb.board, 8)
            time.sleep(0.1)

        self.stop_e.set()

        print("Ended")
        time.sleep(5)
        print_board(self.cb.board, 8)

        self.player_1.join()
        self.player_2.join()

        # print(f" player 1 fitness {self.player_1.fitness(self.cb.board)} player2 fitness {self.player_2.fitness(self.cb.board)}")

        return

    def reset(self):

        self.cb = deepcopy(self.originalBoard)
        # TODO pass to event driven

    def render(self, mode: str = 'unicode') -> str:
        # Shows Chess Board using cli_display

        return board_string(self.cb.board, 8)

    def close(self):
        # Closes enviroment
        self.player_1.join()
        self.player_2.join()

        return

    def win_condition(self):
        # temporary
        if 1+16 not in self.cb.board:
            return -1
        if 1+8 not in self.cb.board:
            return 1
        return 0
