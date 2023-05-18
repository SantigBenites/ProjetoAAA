white_pieces = {
    "Kw": 1+8,  # king
    "Qw": 2+8,  # queen
    "Rw": 3+8,  # rook
    "Bw": 4+8,  # bishop
    "Nw": 5+8,  # knight
    "Pw": 6+8  # pawn
}

black_pieces = {
    "Kb": 1+16,  # king
    "Qb": 2+16,  # queen
    "Rb": 3+16,  # rook
    "Bb": 4+16,  # bishop
    "Nb": 5+16,  # knight
    "Pb": 6+16  # pawn
}

pieces_table = {
    1: "K",  # king
    2: "Q",  # queen
    3: "R",  # rook
    4: "B",  # bishop
    5: "N",  # knight
    6: "P",  # pawn
    0: " ",  # nothin

    8: "W",  # white
    16: "B"  # black
}

print_table = {

}

genotype = {
    "PAWN_VALUE": 1,
    "KNIGHT_VALUE": 1,
    "BISHOP_VALUE": 1,
    "ROOK_VALUE": 1,
    "QUEEN_VALUE": 1,
    "KING_CAPTURE": 1,
    "INFRONT_VALUE": 1,
    "KING_LOSS": 1,
    "KING_ATACK": 1,
    "QUEEN_ATACK": 1,
    "CAPTURE_VALUE": 1,
    "EDGE_VALUE": 1
}


fitness_values = {
    "KING_VALUE": 2000,
    "K": 521,
    "Q": 1710,
    "R": 824,
    "B": 572,
    "N": 521
}
