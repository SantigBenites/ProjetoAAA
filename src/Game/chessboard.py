from Game.moveGeneration import possible_moves
from copy import deepcopy
from Game.moveGeneration import distance_to_edge
import time
import itertools


class Chessboard():

    def __init__(self, board: list[int], cooldown: float, render_mode=None):

        distance_to_edge()
        self.cooldown = cooldown

        # All board states
        self.board_states = []

        # In use
        self.board = board
        self.timestamps = [int(time.time()) - self.cooldown - 1] * 64

    # Step

    def step(self, action: tuple[int, int], player: int):
        """Step represents a discrete action on the board
           The player is the one who is making the action,
           and is the one calling this function
        Args:
            action (tuple[int,int]): tuple of 2 ints, representative of initial piece index and final piece index
            player (int): _description_

        Returns:
            _type_: something to be decided
        """
        # TODO pls i don't remember this ? The index is 0-63 or else?
        current_index, final_index = action
        self.move(current_index, final_index)

        # TODO since we have list[int] do we really need to do deepcopy?
        #! the faster this line is, the better since it will be called a lot
        self.board_states.append(deepcopy(self.board))

        # TODO since we only get experience after the game is over, do we really need to return anything?
        # ? ie, at the end of the game we just need to update the reward of the LAST move on the winning side

        return

    def move(self, current_index: int, final_index: int):
        """Moves a certain piece from current_index to final_index

        Args:
            current_index (int): initial index of piece
            final_index (int): end index of piece
        """
        self.board[final_index] = self.board[current_index]
        self.board[current_index] = 0

        self.timestamps[final_index] = int(time.time())

    def destroyEnemyKing(self, player: int):
        """Used by stockFish to circumvent checkmate logic"""

        if player == 1:
            # 1+16
            self.board[self.board.index(1+16)] = 0
        else:
            # 1+8
            print("removed 1+8")
            self.board[self.board.index(1+8)] = 0

        return

    def legal_moves(self, color) -> list[tuple[int, int]]:
        """Legal moves for the current player."""

        legal_moves = []
        my_pieces = list(filter(lambda index: (self.board[index] >> 3 == color), range(0, 64)))

        
        for piece in my_pieces:
            legal_moves.append(self.valid_moves(piece))

        return list(itertools.chain(*legal_moves))

    def valid_moves(self, index: int) -> list[tuple[int,int]]:
        """Valid moves returns the valid moves for the piece in index

        Args:
            index (int): index in the board of the piece we want to analyze

        Returns:
            list[int]: indexes of all end positions of the piece in index
        """
        current_time = int(time.time())

        if current_time - self.timestamps[index] >= self.cooldown:
            pm = possible_moves(self.board, index)
            return list(zip([index]*len(pm), pm))
        return []

    def pieceOnCooldown(self, index: int) -> bool:
        """Check if the piece located in index is in cool down

        Args:
            index (int): index of the piece we want to check

        Returns:
            bool: bool representative if the piece in index is on cool down
        """
        current_time = int(time.time())
        return True if current_time - self.timestamps[index] >= self.cooldown else False

    def reward(self, player) -> int:
        """Reward of the current board for player

        Args:
            player (_type_): player color we want to analyze, if white  1 else black

        Returns:
            int: 1 of player won, -1 if player lost and 0 if draw
        """
        if player == 1:
            if 1+16 not in self.board:
                return 1
            if 1+8 not in self.board:
                return -1
        else:
            if 1+16 not in self.board:
                return -1
            if 1+8 not in self.board:
                return 1
        return 0

    def move_sim(self, piece_index: int, move_location_index):
        copy = self.board.copy()

        copy[move_location_index] = copy[piece_index]
        copy[piece_index] = 0

        return copy
