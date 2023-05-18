from typing import Iterator, Iterable, LiteralString
from functools import cache

pieces_table = {
    # "♔"
    8 + 1: "W",  # w king
    8 + 2: "♕",  # w queen
    8 + 3: "♖",  # w rook
    8 + 4: "♗",  # w bishop
    8 + 5: "♘",  # w knight
    8 + 6: "♙",  # w pawn

    # "♚"
    16 + 1: "B",  # b king
    16 + 2: "♛",  # b queen
    16 + 3: "♜",  # b rook
    16 + 4: "♝",  # b bishop
    16 + 5: "♞",  # b knight
    16 + 6: "♟",  # b pawn

    0: " ",  # nothin
}


def translate(board):
    return [pieces_table[p] for p in board]


def ranks(board: list[str], board_size: int) -> Iterator[list]:
    """A generator that yields the ranks of a chessboard with size board_size
       Should be called after translate

    Args:
        board (Iterable): the board, a unidimentional iterable
        board_size (int): the size of the board

    Yields:
        Iterator[list]: The next rank of the board
    """
    for rank_index in range(board_size):
        rank_start = rank_index * board_size
        rank_end = rank_start + board_size
        yield board[rank_start:rank_end]


def chunks(array: Iterable, size: int) -> Iterator[list]:
    """A generator that yields chunks with a given size.
        Assumes: 
            len(array) % size == 0 && size > 0

    Args:
        array (Iterable): Any iterable
        size (int): Any int bigger than 0

    Yields:
        Iterator[list]: A list containing the next size
        elements of the array
    """
    for i in range(size):
        start = i * size
        end = start + size
        yield array[start:end]


@cache
def board_divisions(cell_size: int, cell_count: int) -> tuple[str, str, str, LiteralString]:
    """Generates the rows needed to print a board cleanly
        Expects cell_size and cell_count to be bigger than one 
    Args:
        cell_size (int): Size of the contents of a cell
        cell_count (int): How many cells in a row

    Returns:
        tuple[str]: A touple containing the strings
    """
    cell_size = cell_size + 2

    top = ('┏' + (('━'*(cell_size) + '┳') * cell_count))[:-1] + '┓'
    middle = ('┣' + (('━'*(cell_size) + '╋') * cell_count))[:-1] + '┫'
    bottom = ('┗' + (('━'*(cell_size) + '┻') * cell_count))[:-1] + '┛'

    spacer = (" " * (cell_size//2))
    empty_row = (("|" + spacer + "{}" + spacer) * cell_count) + "|"

    return top, middle, bottom, empty_row


def print_board(board: Iterable, size: int):
    """Prints a unidimentional array as a game board \n
    Assumes len(board) % size == 0

    Args:
        board (Iterable): Any iterable
        size (int): _description_
    """

    n_board = translate(board)

    top, middle, bottom, empty_row = board_divisions(1, size)

    rep = [top]

    for rank in ranks(n_board, size):
        rep.append(empty_row.format(*rank))
        rep.append(middle)

    rep[-1] = bottom
    # import os
    # os.system('clear')
    print(*rep, sep="\n", flush=True)


def board_string(board: Iterable, size: int):
    """Returns a string representative of the chess board current State"""

    n_board = translate(board)

    top, middle, bottom, empty_row = board_divisions(1, size)

    rep = [top]

    for rank in ranks(n_board, size):
        rep.append(empty_row.format(*rank))
        rep.append(middle)

    rep[-1] = bottom

    return rep
