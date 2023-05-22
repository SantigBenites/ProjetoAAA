import os
import string
import threading
import chess.engine
import random

from Game.chessboard import Chessboard
from chess.engine import EngineTerminatedError
from lib.typedef import SFPlayerConfig

timeScale = 2.0


ENGINEPATH = os.getcwd() + "/assets/stockfish-ubuntu-20.04-x86-64"

class StockFishPlayer(threading.Thread):

    def __init__(self, config: SFPlayerConfig, c_board: Chessboard, stop: threading.Event) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.cb = c_board
        self.color = config.color
        self.engine = chess.engine.SimpleEngine.popen_uci(ENGINEPATH)
        self.stop = stop

    # def __init__(self, c_board: Chessboard, color: int, stop: threading.Event) -> None:
    #    threading.Thread.__init__(self, daemon=True)
    #    self.cb = c_board
    #    self.stop = stop
    #    self.color = color
    #    self.engine = chess.engine.SimpleEngine.popen_uci(ENGINEPATH)

    def run(self) -> None:
        
        while not self.stop.is_set():
            mv = self.choose_next_move()
            # time.sleep(0.2)
            if mv != None:
                self.cb.step(mv, self.color)

        try:
            self.engine.quit()
        except EngineTerminatedError:
            # Engine terminated just assume things went wrong somewhere
            pass


    def choose_next_move(self) -> None | tuple[int,int]:
        """Choose next move for StockFish player based on the StockFish engine

        Returns:
            None | tuple[int,int]: Returns the best move the player can do based on the StockFish engine, or returns None if the king is either in checkmate or dead
        """
        # board - player - castle - enPasssant - halfMove - fullmove

        legal_moves = self.cb.legal_moves(self.color)
        enemy_king = 1+8 if self.color == 2 else 1+16
        try:
            enemy_king_index = self.cb.board.index(enemy_king)
        except ValueError:
            return None
        king_in_check = [x for x in legal_moves if x[1] == enemy_king_index]
        if king_in_check != []:
            return random.choice(king_in_check)

        board = chess.Board(fen=self.boardToFen())
        try:
            result = self.engine.play(board, chess.engine.Limit(timeScale))
        except chess.engine.EngineTerminatedError:
            return None

        best_move = result.move

        return self.standardMoveToLocation(str(best_move))

    def standardMoveToLocation(self, move) -> None | tuple[int,int]:

        if move == None:
            return None

        row1, col1, row2, col2 = move[0], int(move[1]), move[2], int(move[3])

        row1 = string.ascii_lowercase.index(row1)+1
        row2 = string.ascii_lowercase.index(row2)+1

        return ((col1-1)*8 + row1-1, (col2-1)*8 + row2-1)

    def getPiece(self, value):

        match value:
            case 9:  # 1+8
                return "k"
            case 10:  # 2+8
                return "q"
            case 11:  # 3+8
                return "r"
            case 12:  # 4+8
                return "b"
            case 13:  # 5+8
                return "n"
            case 14:  # 6+8
                return "p"
            case 17:  # 1+16
                return "K"
            case 18:  # 2+16
                return "Q"
            case 19:  # 3+16
                return "R"
            case 20:  # 4+16
                return "B"
            case 21:  # 5+16
                return "N"
            case 22:  # 6+16
                return "P"
            case 0:
                return 0

    def boardToFen(self):
        string = ""
        empty = 0
        for index, square in enumerate(self.cb.board):

            piece = self.getPiece(square)

            if piece == 0:
                empty += 1
            else:
                if empty:
                    string += str(empty)
                    empty = 0
                string += piece

            if index % 8 == 7:
                if empty:
                    string += str(empty)
                    empty = 0

                if index != 63:
                    string += "/"

        # String represents the board

        # Add color
        string += " w " if self.color == 1 else " b "

        # Add castling (irrelevant)
        string += " KQkq "

        # Add en passant
        string += " - "

        # Add Halfmove Clock
        string += " 0 "

        # Add Full moves (TODO, i think this is necessary)
        string += " 1 "
        return string
