from lib.typedef import RunConfig

_BOARD = [3+8, 5+8, 4+8, 2+8, 1+8, 4+8, 5+8, 3+8,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0,
          3+16, 5+16, 4+16, 2+16, 1+16, 4+16, 5+16, 3+16
          ]

_GA_GENOTYPE = {
    'PAWN_VALUE': 3380,
    'KNIGHT_VALUE': 3349,
    'BISHOP_VALUE': 116,
    'ROOK_VALUE': 2704,
    'QUEEN_VALUE': 3350,
    'KING_CAPTURE': 2854,
    'INFRONT_VALUE': 3149,
    'KING_LOSS': 3988,
    'KING_ATACK': 789,
    'QUEEN_ATACK': 501,
    'CAPTURE_VALUE': 1616,
    'EDGE_VALUE': 1051
}

config = RunConfig(
    cooldown=0.1,
    StockFish_episodes=100,
    train_episodes=100,
    pop_size=16,
    base_board=_BOARD,
    ga_genotype=_GA_GENOTYPE,
    time_out=60,
    nn_win_reward=50,
    discount_factor=0.9,
    verbose=False
)
