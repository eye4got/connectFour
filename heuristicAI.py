import numpy as np
import logging
from typing import Union, Tuple, List
from gameBoard import GameBoard

class HeuristicAI:

    def __init__(self, player_num: int):
        self.player_num = player_num

        # Values indicate column of corresponding move (reset
        self.blocking_move = 0
        self.winning_move = 0


    def check_for_final_moves(self, legal_moves: List[int], board: GameBoard):

        curr_legal_move = 0

        while self.winning_move == 0 and curr_legal_move < len(legal_moves):

            curr_row = legal_moves[curr_legal_move]
            row_idx = curr_row - 1
            coords = (row_idx, board.row_heights[row_idx])

            if self.blocking_move == 0:
                self.check_slot_for_final_move(board, coords, self.player_num)
            else:
                self.check_slot_for_final_move(board, coords, self.player_num)

            if self.winning_move != 0:
                curr_legal_move += 1


    def check_slot_for_final_move(self, board: GameBoard, coords: Tuple[int, int], token : int):

        vectors = [(1, 1), (0, 1), (1, -1), (-1, 0)]
        vec_num = 0

        while self.winning_move == 0 and vec_num < len(vectors):
            vector = vectors[vec_num]
            self.check_line_for_final_move(coords, token, vector)

            if self.winning_move == 0:
                vec_num += 1


    def check_line_for_final_move(self, board: GameBoard, coords: Tuple[int, int], token : int, vector: Tuple[int, int]) -> bool:

        # Vector indicates the positive direction of the line being checked
        # First check positive direction
        consec_tokens = self.check_dir_for_tokens(coords, token, vector, 0)

        # Then change vector direction to negative and check
        if vector != (-1, 0):
        vector = (vector[0] * -1, vector[1] * -1)
        consec_tokens = self.check_dir_for_tokens(coords, token, vector, consec_tokens)

        return consec_tokens == 3


    def check_dir_for_tokens(self, coords: Tuple[int, int], token : int, vector: Tuple[int, int], consec_tokens : int) -> int:

        # consec_tokens indicates how many tokens in a line there are
        # token indicates which player *might* be winning and the type of tokens we are looking for

        dir_unbounded = True

        while dir_unbounded and consec_tokens < 3:
            coords = (coords[0] + vector[0], coords[1] + vector[1])

            row_coord_is_illegal = coords[0] > (GameBoard.board_rows - 1) or coords[0] < 0
            col_coord_is_illegal = coords[1] > (GameBoard.board_cols - 1) or coords[1] < 0

            if row_coord_is_illegal or col_coord_is_illegal or self.board[coords[0]][coords[1]] != token:
                dir_unbounded = False

            else:
                consec_tokens += 1

        return consec_tokens