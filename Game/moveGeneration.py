import math
from Game.pieces import pieces_table
from functools import cache
from Game.cli_display import print_board

direction_offsets = [8, -8, 1, -1, 7, -7, 9, -9]
square_to_edge = {}

@cache
def distance_to_edge():

    for x in range(0,8):
        for y in range(0,8):

            square_index = y * 8 + x

            num_north = 7 - y
            num_south = y
            num_west = x
            num_east = 7 - x

            square_to_edge[square_index] = [
                num_north,
                num_south,
                num_east,
                num_west,
                min(num_north,num_west),
                min(num_south,num_east),
                min(num_north,num_east),
                min(num_south,num_west)
                ]


def possible_moves(board, piece_index: int) -> list[int]:
    """Returns all valid moves starting in piece_index for piece of type piece_type

    Args:
        piece_index (int): index of a piece in chess board
        piece_type (str): string representing piece type in index 

    Returns:
        list[int]: all valid moves for that piece starting in piece_index
    """

    piece = board[piece_index]

    color = piece >> 3
    piece_type = pieces_table[piece & 7]

    if piece_type == "Q" or piece_type == "R" or piece_type == "B" : # pieces that slide
        return sliding_moves(board, piece_index, piece_type, color)
    
    if piece_type == "P" :
        return pawn_moves(board,piece_index,color)

    if piece_type == "K" :
        return king_moves(board,piece_index,color)

    if piece_type == "N" :
        return knight_moves(board,piece_index,color)



def sliding_moves(board , piece_index ,piece_type, color):

    valid_directions = direction_offsets.copy()
    square_to_edge_valid = square_to_edge[piece_index]

    if piece_type == "R" :
        valid_directions = valid_directions[0 : 4]
        square_to_edge_valid = square_to_edge_valid[0 : 4]

    if piece_type == "B" :
        valid_directions = valid_directions[4 : 8]
        square_to_edge_valid = square_to_edge_valid[4 : 8]

    valid_moves = []

    for count,dir in enumerate(valid_directions):
        for spaces_to_edge in range(1,square_to_edge_valid[count] + 1):

            index = piece_index + dir * (spaces_to_edge)
            if (board[index] != 0 and board[index] >> 3 == color):
                break
            
            valid_moves.append(index)

            if (board[index] != 0 and board[index] >> 3 != color):
                break

    return valid_moves



def pawn_moves(board, piece_index, color):

    if color == 1:
        move = direction_offsets[0]
        opositecolor = 2
    else:
        move = direction_offsets[1]
        opositecolor = 1
    
    
    rank = math.floor(piece_index / 8)
    valid_moves = []

    if board[piece_index + move] == 0:
        valid_moves = [piece_index + move]

    if board[piece_index + move + 1] >> 3 == opositecolor:
        valid_moves.append(piece_index + move + 1)
    
    if board[piece_index + move - 1] >> 3 == opositecolor:
        valid_moves.append(piece_index + move - 1)

    if (rank in [1, 6]) and (0 <= piece_index + move*2 <= 63) :

        new_index = piece_index + move*2

        if (board[new_index] == 0):
            valid_moves.append(new_index)
        

    return valid_moves


def king_moves(board,piece_index,color):

    valid_moves = []

    for count,dir in enumerate(direction_offsets):
        spaces_to_edge = square_to_edge[piece_index][count]
        if spaces_to_edge > 0:
            
            if (board[piece_index + dir] == 0):
                valid_moves.append(piece_index + dir)

            if (board[piece_index + dir] != 0 and board[piece_index + dir] >> 3 != color):
                valid_moves.append(piece_index + dir)
            

    return valid_moves


def knight_moves(board,piece_index,color):

    valid_moves = []

    possible_moves = [10,17,15,6,-10,-17,-15,-6]

    needed_space = [(1,0,2,0),(2,0,1,0),(2,0,0,1),(1,0,0,2),(0,1,0,2),(0,2,0,1),(0,2,1,0),(0,1,2,0)]

    for count,dir in enumerate(possible_moves):
        offsets = square_to_edge[piece_index]
        needed = needed_space[count]
        if (offsets[0] >= needed[0] and 
            offsets[1] >= needed[1] and 
            offsets[2] >= needed[2] and 
            offsets[3] >= needed[3] ):


            if (board[piece_index + dir] == 0):
                valid_moves.append(piece_index + dir)

            if (board[piece_index + dir] != 0 and board[piece_index + dir] >> 3 != color):
                valid_moves.append(piece_index + dir)


    return valid_moves
