import chess.engine
import Game.pieces
from Game.chess import Chessboard 
import time



engine = chess.engine.SimpleEngine.popen_uci("/home/santig/Programs/StockFish/stockfish-ubuntu-20.04-x86-64")

# board - player - castle - enPasssant - halfMove - fullmove
board = chess.Board(fen = "rnbqkbnr/8/8/1B6/8/8/3N4/R1BQK1NR w  KQkq  -  0  1")
#("RN1KQBNR/8/8/8/6B1/8/8/rnbkqbnr w - - 0 1")

print(board)
result = engine.play(board, chess.engine.Limit(time=2.0))
best_move = result.move

print(best_move)

board.push(best_move)

print(board)
engine.quit()
