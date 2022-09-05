import numpy as np
import logging
from typing import Union, Tuple, List

class GameBoard:

    board_rows = 6
    board_cols = 7

    def __init__(self):
        # The Board is represented by an array with 7 columns and 6 rows
        # (0, 0) corresponds to the bottom left corner
        # 0 indicates an empty space, 1 indicates player one's token, 2 player two's token
        self.board = np.zeros(shape = (GameBoard.board_rows, GameBoard.board_cols), dtype=np.int8)
        self.move_num : int = 0 # Counts total number of moves (two per round)
        self.is_complete : bool = False

        # Keep track of player moves and result to assist with decision analysis
        self.player_one_moves : List[int] = []
        self.player_two_moves : List[int] = []
        self.row_heights : List[int] = [0] * GameBoard.board_cols
        # Legal moves is stored as its own variable to avoid unnecessary duplicate calculations
        self.legal_moves = list(range(1, GameBoard.board_cols + 1))
        self.victor : Union[None, int] = None
        self.victory_direction : str = ""

    def __repr__(self) -> str:
        output_board = np.flip(self.board, axis = 0)
        #TODO: remove 0s
        return str(output_board)


    def add_piece(self, column: int):

        # Check if desired move is legal
        if column < 1 or column > self.board_cols:
            raise ValueError(f"Piece insertion column must be between 1 and 7, {column} is incorrect")

        col_idx = column - 1 # Indexes refer to array position, while standard value uses 1-based counting
        if self.row_heights[col_idx] == self.board_rows:
            raise ValueError(f"Piece insertion must be on a column with empty slots, column: {column} is full")

        # Current player token is worked out based on odd/even move number, player one starts
        token = 1
        if self.move_num % 2 == 1:
            token = 2

        # Only column input is provided. Row height is calculated based on previous highest token in that column
        row_idx = self.row_heights[col_idx]
        self.board[row_idx][col_idx] = token

        # Store legal move
        if token == 1:
            self.player_one_moves.append(column)
        else:
            self.player_two_moves.append(column)

        self.move_num += 1
        self.row_heights[col_idx] += 1
        if self.row_heights[col_idx] == GameBoard.board_rows:
            self.legal_moves.remove(col_idx + 1)

        logging.debug(f"Move: {self.move_num}, Player {token} @ column {column}, row {row_idx + 1}")
        logging.debug(self)

        move_result = self.check_victory((row_idx, col_idx), token)

        # All other move results (except 'No Victor') indicate a winning move, so capture victory and wrap up board
        if move_result != "No Victor":
            self.victor = token
            self.victory_direction = move_result
            self.is_complete = True
            logging.info(f"Player {token} wins, {self.victory_direction} with final move at column {column}, "
                         f"row {row_idx + 1} (Move: {self.move_num})")

        # Check for stalemate (all slots on the board have been filled)
        elif self.move_num == (GameBoard.board_rows * GameBoard.board_cols):
            logging.debug(self)
            logging.info(f"Game ends in a Stalemate (Move: {self.move_num})")
            self.is_complete = True


    def check_victory(self, coords: Tuple[int, int], token : int) -> str:

        result = "No Victor"
        is_victory = False
        vectors = [(1, 1), (0, 1), (1, -1), (-1, 0)]
        vec_names = ["Diagonal Up", "Horizontal", "Diagonal Down", "Vertical"]
        vec_num = 0

        while not is_victory and vec_num < len(vectors):
            vector = vectors[vec_num]
            is_victory = self.check_line_for_victory(coords, token, vector)

            if not is_victory:
                vec_num += 1

        if is_victory:
            result = vec_names[vec_num]

        return result


    def check_line_for_victory(self, coords: Tuple[int, int], token : int, vector: Tuple[int, int]) -> bool:

        # Vector indicates the positive direction of the line being checked
        # First check positive direction
        consec_tokens = self.check_dir_for_tokens(coords, token, vector, 0)

        # Then change vector direction to negative and check
        # No need to check upward vertical (Reduced time by 7% when tested on 300,000 games)
        if vector != (-1, 0):
            vector = (vector[0] * -1, vector[1] * -1)
            consec_tokens = self.check_direction_for_tokens(coords, token, vector, consec_tokens)

        return consec_tokens == 3


    def check_direction_for_tokens(self, coords: Tuple[int, int], token : int, vector: Tuple[int, int], consec_tokens : int) -> int:

        #   consec_tokens indicates how many tokens in a line there are. We pass this in to ensure we halt early, if
        #       enough tokens have been accumulated from the other side
        #   token indicates which player *might* be winning and the type of tokens we are looking for

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