import chess.engine
from Game.chess import Chessboard 
import time

cooldown = 1

board = [3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         0,0,0,0,0,0,0,0,
         3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
        ]

cb = Chessboard(
    board,                                  
    [int(time.time()) - cooldown - 1] * 64, 
    cooldown                                
)
rows,cols = 8,8
string = ""

for row in range(rows):

    emptySpace = 0

    for col in range(cols):

        currentVal = cb.board[row*8 + col]
            
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

string = string[:-1]



engine = chess.engine.SimpleEngine.popen_uci("/home/santig/Programs/StockFish/stockfish-ubuntu-20.04-x86-64")

# board - player - castle - enPasssant - halfMove - fullmove
board = chess.Board(fen = string)
#"rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w - c6 0 1")

result = engine.play(board, chess.engine.Limit(time=2.0))
best_move = result.move

print(best_move)

board.push(best_move)

print(board)

engine.quit()
