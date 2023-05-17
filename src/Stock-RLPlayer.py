import time
from StockFish.StockFishplayer import StockFishPlayer
from ReiforcementLearning.RLplayer import RLPlayer
from Game.chess import Game
from Game.chessboard import Chessboard
import threading as td

# Game vars
board =[3+8,5+8,4+8,2+8,1+8,4+8,5+8,3+8,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        3+16,5+16,4+16,2+16,1+16,4+16,5+16,3+16
        ]
cooldown = 0.01

# End event
stop_e = td.Event()

# Board
cb = Chessboard(board,cooldown * 64,cooldown)

# Players
p1 = RLPlayer(cb, 1, stop_e)
p2 = StockFishPlayer(cb, 2, stop_e)

# Game
chess = Game(p1,p2,cb,stop_e)


chess.play(verbatim=True)