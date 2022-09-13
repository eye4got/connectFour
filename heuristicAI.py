import numpy as np
import numpy.typing as npt
import logging
import random
from typing import Union, Tuple, List

class HeuristicAI:

    def __init__(self, player_num: int, board_rows: int = 6, board_cols: int = 7):
        if not(player_num == 1 or player_num == 2):
            raise ValueError("Player Number must be 1 or 2")

        self.player_num = player_num
        self.opponent_num = 1 if player_num == 2 else 1

        # Player needs to know dimensions of board
        # Players that use NNs will only be able to play with specific board dimensions anyway
        self.board_rows = board_rows
        self.board_cols = board_cols


    def choose_move(self, board: npt.ArrayLike, legal_moves: List[int], row_heights: List[int]):

        curr_legal_move = 0
        col_of_highest_consec_move = random.choice(legal_moves) # Random seed for starting move
        highest_consec_count = 0
        col_of_blocking_move = 0
        found_winning_move = False

        # Keep looking until you find a winning move or are out of moves to check, record blocking moves in case
        while not found_winning_move and curr_legal_move < len(legal_moves):

            # Identify next legal move and its corresponding coords
            curr_col = legal_moves[curr_legal_move]
            col_idx = curr_col - 1
            coords = (row_heights[col_idx], col_idx)

            # Check the number of contiguous pieces that would be achieved by playing the current legal move
            curr_col_count = self.check_slot_for_consec_tokens(board, coords, self.player_num)
            logging.debug(f"Consec count: {curr_col_count} for col: {col_idx}")

            # Check if it's a winning move or at least better than the previous best move
            # The greater than comparison preferences moves to the left, perhaps this should be changed to preference
            # centre moves?
            if curr_col_count == 3:
                found_winning_move = True
            elif curr_col_count > highest_consec_count:
                col_of_highest_consec_move = curr_col
                highest_consec_count = curr_col_count

            # If you haven't found a winning move or a blocking move (default value of 0), check for blocking move
            if not found_winning_move and col_of_blocking_move == 0:
                curr_block_col = self.check_slot_for_consec_tokens(board, coords, self.opponent_num)
                if curr_block_col == 3:
                    col_of_blocking_move = curr_col
                    logging.info(f"Found blocking move: {curr_col}")

            curr_legal_move += 1

        # Play winning move, else block opponents winning move, else play move with most contiguous counters
        if found_winning_move:
            move = curr_col
        elif col_of_blocking_move != 0:
            move = col_of_blocking_move
        else:
            move = col_of_highest_consec_move

        return move


    def check_slot_for_consec_tokens(self, board: npt.ArrayLike, coords: Tuple[int, int], token : int) -> int:
        """
        Determines the number of tokens of the current player lined up with the specified slot before anything is placed

        :param board: a two-dimensional array matching the class row/height, with 0 for empty and 1 or 2 for player tokens
        :param coords: the coordinates of the current move to assess
        :param token: number of the current player (must be 1 or 2 to match board representation)
        :return: number of contiguous tokens along one of the lines intersecting with coords on the board
        """

        vectors = [(1, 1), (0, 1), (1, -1), (-1, 0)]
        vec_num = 0
        max_consec_tokens = 0

        # While winning/blocking move hasn't been identified and there are still more vectors to check
        while max_consec_tokens < 3 and vec_num < len(vectors):
            vector = vectors[vec_num]
            # Check if current vector has more tokens than previous, and if so, store the count
            max_consec_tokens = max(max_consec_tokens, self.check_line_for_consec_tokens(board, coords, token, vector))

            if max_consec_tokens != 3:
                vec_num += 1

        return max_consec_tokens


    def check_line_for_consec_tokens(self, board: npt.ArrayLike, coords: Tuple[int, int], token : int, vector: Tuple[int, int]) -> int:

        # Vector indicates the positive direction of the line being checked
        # First check positive direction
        consec_tokens = self.check_dir_for_tokens(board, coords, token, vector, 0)

        # Then change vector direction to negative and check
        if vector != (-1, 0):
            vector = (vector[0] * -1, vector[1] * -1)
            consec_tokens = self.check_dir_for_tokens(board, coords, token, vector, consec_tokens)

        return consec_tokens


    def check_dir_for_tokens(self, board: npt.ArrayLike, coords: Tuple[int, int], token : int, vector: Tuple[int, int], consec_tokens : int) -> int:

        """
        Checks the number of tokens belonging to a player in a specific direction (one of eight) until it hits blanks,
        boundaries or the opposite players tokens.

        :param board: a two-dimensional array matching the class row/height, with 0 for empty and 1 or 2 for player tokens
        :param coords: the coordinates of the current move to assess
        :param token: number of the current player (must be 1 or 2 to match board representation)
        :param vector:
        :param consec_tokens:
        :return:
        """
        # consec_tokens indicates how many tokens in a line there are
        # token indicates which player *might* be winning and the type of tokens we are looking for

        dir_bounded = False
        curr_coords = coords

        while not dir_bounded and consec_tokens < 3:
            curr_coords = (curr_coords[0] + vector[0], curr_coords[1] + vector[1])

            row_coord_is_illegal = curr_coords[0] > (self.board_rows - 1) or curr_coords[0] < 0
            col_coord_is_illegal = curr_coords[1] > (self.board_cols - 1) or curr_coords[1] < 0

            if row_coord_is_illegal or col_coord_is_illegal or board[curr_coords[0]][curr_coords[1]] != token:
                dir_bounded = True

            else:
                consec_tokens += 1

        return consec_tokens