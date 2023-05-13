import chess.engine
import Game.pieces
from Game.chess import Chessboard 
import time


cooldown = 1

board = [3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,4+16,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         3+16,5+16,4+16,2+16,1+16,0,5+16,3+16
        ]

cb = Chessboard(
    board,                                  
    [int(time.time()) - cooldown - 1] * 64, 
    cooldown                                
)


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

string = ""
empty = 0
for index,square in enumerate(board):
    
    piece = getPiece(square)

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

string +=  " w KQkq - 0 1"

print(string)



engine = chess.engine.SimpleEngine.popen_uci("/home/santig/Programs/StockFish/stockfish-ubuntu-20.04-x86-64")

# board - player - castle - enPasssant - halfMove - fullmove
board = chess.Board(fen = string)
#("RN1KQBNR/8/8/8/6B1/8/8/rnbkqbnr w - - 0 1")

#result = engine.play(board, chess.engine.Limit(time=2.0))
#best_move = result.move

#print(best_move)

#board.push(best_move)

print(board)

engine.quit()
