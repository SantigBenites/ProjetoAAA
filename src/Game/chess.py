import time
import random
import threading as td
import multiprocessing as mp

from copy import deepcopy
from attrs import define, field
from Game.chessboard import Chessb
from Game.chessboard import Chessboard
from Game.cli_display import print_board, board_string

TIME_OUT = 100
NN_WIN_REWARD: int = 50  # reward for the winning move
DISCOUNT_FACTOR: float = 0.9  # discount factor for the reward


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

    def play(self, verbatim: bool = False):

        start_time = int(time.time())
        curr_time = int(time.time())

        self.player_1.start()
        self.player_2.start()

        # and (start_time + TIME_OUT > curr_time):
        while ((1+8 in self.cb.board) and (1+16 in self.cb.board)): #and (start_time + TIME_OUT > curr_time)):
            curr_time = int(time.time())
            if verbatim:
                print_board(self.cb.board, 8)
            time.sleep(0.1)

        self.stop_e.set()
        print_board(self.cb.board, 8)

        self.player_1.join()
        self.player_2.join()

        # print(f" player 1 fitness {self.player_1.fitness(self.cb.board)} player2 fitness {self.player_2.fitness(self.cb.board)}")

        winner = 2 if 1+8 not in self.cb.board else 1
        self.winner = winner

        white_x: list[Chessb] = []
        white_y: list[float] = []
        black_x: list[Chessb] = []
        black_y: list[float] = []

        self.cb.board_states.reverse()
        reward = NN_WIN_REWARD

        for board, player in self.cb.board_states:
            r = reward if player == winner else 0
            if player == 1:
                white_x.append(board)
                white_y.append(r)
            else:
                black_x.append(board)
                black_y.append(r)
            reward *= DISCOUNT_FACTOR  # the first reward should be the full reward

        return white_x, white_y, black_x, black_y

    def win_condition(self):
        # temporary
        if 1+16 not in self.cb.board:
            return -1
        if 1+8 not in self.cb.board:
            return 1
        return 0
