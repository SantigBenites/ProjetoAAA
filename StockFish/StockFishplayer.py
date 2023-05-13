import threading, gym, random, time, string

from Game.pieces import pieces_table
from Game.moveGeneration import possible_moves
from Game.chessboard import Chessboard
from Game.cli_display import board_string
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("/home/santig/Programs/StockFish/stockfish-ubuntu-20.04-x86-64")
timeScale = 2.0

class StockFishPlayer(threading.Thread):

    def __init__(self, c_board: Chessboard, color: int, stop: threading.Event) -> None:
        threading.Thread.__init__(self, daemon=True) 
        self.cb = c_board
        self.stop = stop
        self.color = color

    def run(self) -> None:
        while not self.stop.is_set():
            mv = self.choose_net_move()
            time.sleep(0.1)
            self.cb.step(mv)

    def choose_net_move(self):

        # board - player - castle - enPasssant - halfMove - fullmove
        board = chess.Board(fen = self.boardToFen())

        result = engine.play(board, chess.engine.Limit(timeScale))
        best_move = result.move

        return self.standardMoveToLocation(best_move)
    
    def standardMoveToLocation(self, move):

        row1, col1, row2, col2 = move[0], move[1], move[3], move[4]

        col1 = string.lowercase.index(col1)
        col2 = string.lowercase.index(col2)

        return (row1 + col1 * 8, row2 + col2 * 8)

    def getPiece(int):

        match int:
            case 9 : #1+8 
                return "k"
            case 10: #2+8 
                return "q"
            case 11: #3+8 
                return "r"
            case 12: #4+8 
                return "b"
            case 13: #5+8
                return "n"
            case 14: #6+8
                return "p"
            case 17: #1+16 
                return "K"
            case 18: #2+16
                return "Q"
            case 19: #3+16
                return "R"
            case 20: #4+16
                return "B"
            case 21: #5+16
                return "N"
            case 22: #6+16
                return "P"
            case 0:
                return 0
            
    def boardToFen(self):
        string = ""
        empty = 0
        for index,square in enumerate(self.cb.board):
            
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

        # String is board
        string +=  "KQkq - 0 1"

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