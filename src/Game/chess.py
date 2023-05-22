import time
import threading as td

from lib.typedef import PlayerDef, GameReturn
from lib.constants import config
from Game.chessboard import Chessboard
from Game.cli_display import print_board
from lib.constants import config

from GeneticAlgorythm.GAPlayer import GAPlayer
from ReinforcementLearning.RLplayer import RLPlayer
from StockFish.StockFishplayer import StockFishPlayer

player_map = {
    "RL": RLPlayer,
    "GA": GAPlayer,
    "SF": StockFishPlayer
}


class Game:
    def __init__(self, player1: PlayerDef, player2: PlayerDef):
        self.stop_e = td.Event()
        self.cb = Chessboard(config.base_board.copy(), config.cooldown)
        self.player_1 = player_map[player1.type](
            player1.config, self.cb, self.stop_e)
        self.player_2 = player_map[player2.type](
            player2.config, self.cb, self.stop_e)

    def play(self, verbatim: bool = False):

        self.player_1.start()
        self.player_2.start()

        start_time = int(time.time())
        curr_time = int(time.time())

        # and (start_time + TIME_OUT > curr_time):
        # and (start_time + TIME_OUT > curr_time)):
        while ((1+8 in self.cb.board) and (1+16 in self.cb.board) and (start_time + config.time_out > curr_time)):
            curr_time = int(time.time())
            if verbatim:
                print_board(self.cb.board, 8)
            time.sleep(0.1)

        self.stop_e.set()

        print('[GAME]', f'Before Joining threads', flush=True)

        self.player_1.join()
        self.player_2.join()
        # print_board(self.cb.board, 8)
        self.duration = curr_time - start_time

        white_x: list[list[int]] = []
        white_y: list[float] = []
        black_x: list[list[int]] = []
        black_y: list[float] = []

        if self.duration >= config.time_out:
            for board, player in self.cb.board_states:
                r = 0
                if player == 1:
                    white_x.append(board)
                    white_y.append(r)
                else:
                    black_x.append(board)
                    black_y.append(r)

            return GameReturn(white_x,
                              white_y,
                              black_x,
                              black_y,
                              self.duration,
                              len(self.cb.board_states),
                              1)

        if 1+8 not in self.cb.board: 
            winner = 2 
        elif 1+16 not in self.cb.board:
            winner = 1
        else:
            winner = 0

        self.winner = winner

        white_x: list[list[int]] = []
        white_y: list[float] = []
        black_x: list[list[int]] = []
        black_y: list[float] = []

        self.cb.board_states.reverse()
        reward = config.nn_win_reward

        for board, player in self.cb.board_states:
            r = reward if player == winner else 0
            if player == 1:
                white_x.append(board)
                white_y.append(r)
            else:
                black_x.append(board)
                black_y.append(r)
            reward *= config.discount_factor

        print('[GAME]', f'game ended with winner {winner}', flush=True)

        return GameReturn(white_x,
                          white_y,
                          black_x,
                          black_y,
                          self.duration,
                          len(self.cb.board_states),
                          winner)

    def win_condition(self):
        # temporary
        if 1+16 not in self.cb.board:
            return -1
        if 1+8 not in self.cb.board:
            return 1
        return 0
