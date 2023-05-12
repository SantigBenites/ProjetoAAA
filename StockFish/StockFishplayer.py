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
            self.move(mv[0], mv[1])

    def step(self, action: tuple[int,int]) -> None:

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

    def boardToFen(self):
        rows,cols = 8,8
        string = ""

        for row in range(rows):

            emptySpace = 0

            for col in range(cols):

                currentVal = self.cb.board[row*8 + col]
                    
                if emptySpace != 0 and currentVal != 0:
                    string += str(emptySpace)

                match currentVal:
                    case 9 : #1+8 
                        string += "k"
                    case 10: #2+8 
                        string += "q"
                    case 11: #3+8 
                        string += "r"
                    case 12: #4+8 
                        string += "b"
                    case 13: #5+8
                        string += "n"
                    case 14: #6+8
                        string += "p"
                    case 17: #1+16 
                        string += "K"
                    case 18: #2+16
                        string += "Q"
                    case 19: #3+16
                        string += "R"
                    case 20: #4+16
                        string += "B"
                    case 21: #5+16
                        string += "N"
                    case 22: #6+16
                        string += "P"
                    case 0:
                        emptySpace+=1

            if emptySpace != 0:
                string += str(emptySpace)
            string += "/"

        return string[:-1]