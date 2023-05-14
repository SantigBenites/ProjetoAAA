import time
from StockFish import StockFishplayer
from Game.chess import Game
from Game.chessboard import Chessboard

board =[3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
        ]

chess = Game(board,0.01)

chess.play(verbatim=True)
