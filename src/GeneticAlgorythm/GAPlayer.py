import threading
import random
import time


from lib.typedef import GAPlayerConfig
from Game.pieces import pieces_table
from Game.chessboard import Chessboard
from Game.cli_display import board_string
from Game.moveGeneration import possible_moves, square_to_edge


class GAPlayer(threading.Thread):

    def __init__(self, config: GAPlayerConfig) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.cb = config.c_board
        self.stop = config.stop
        self.color = config.color
        self.genotype = config.genotype

    def run(self) -> None:

        while not self.stop.is_set():

            mv = self.choose_next_move()

            if mv != None:

                self.cb.step(mv, self.color)

    def choose_next_move(self) -> None | tuple[int, int]:

        # TODO play function
        current_moves = self.cb.legal_moves(self.color)
        move_values = []
        for move in current_moves:

            pred_value = self.eval_function(move[0], move[1])
            move_values.append((move, pred_value))

        if len(move_values) == 0:
            return None
        max_move, max_value = max(move_values, key=lambda x: x[1])

        return max_move

    def random_move(self):
        moves = self.cb.legal_moves(self.color)
        if moves:
            return random.choice(moves)
        else:
            return None

    def eval_function(self, piece_index, move_index):

        # Board after move
        new_board = self.cb.move_sim(piece_index, move_index)
        # Variables
        state_score = 0
        piece_values = {1: 0,
                        2: self.genotype["QUEEN_VALUE"],
                        3: self.genotype["ROOK_VALUE"],
                        4: self.genotype["BISHOP_VALUE"],
                        5: self.genotype["KNIGHT_VALUE"],
                        6: self.genotype["PAWN_VALUE"]}
        my_king = 1+8 if self.color == 1 else 1+16
        oposite_king = 1+16 if self.color == 1 else 1+8
        oposite_queen = 2+16 if self.color == 1 else 2+8
        valid_moves = self.cb.valid_moves(move_index)
        atacked_pieces = [new_board[i[1]]
                          for i in valid_moves] if valid_moves != [] else []

        # Scoring
        if self.color == 1:
            state_score += self.genotype["INFRONT_VALUE"] if move_index > piece_index else 0
        else:
            state_score += self.genotype["INFRONT_VALUE"] if move_index < piece_index else 0

        state_score -= self.genotype["KING_LOSS"] if new_board[move_index] == my_king else 0
        state_score += self.genotype["KING_ATACK"] if oposite_king in atacked_pieces else 0
        state_score -= self.genotype["QUEEN_ATACK"] if oposite_queen in atacked_pieces else 0
        state_score += self.genotype["KING_CAPTURE"] if new_board[move_index] == oposite_king else 0
        state_score += self.genotype["CAPTURE_VALUE"] if new_board[move_index] >> 3 != self.color else 0

        for index in range(0, 63):
            piece = new_board[index]

            if piece != 0:

                edges = square_to_edge[index]

                if self.color == piece >> 3:
                    state_score += piece_values[piece & 7]
                    state_score -= self.genotype["EDGE_VALUE"] if edges[0] < 2 or edges[1] < 2 or edges[3] < 2 or edges[4] < 2 else 0

                if self.color != piece >> 3:
                    state_score -= piece_values[piece & 7]

        return state_score
