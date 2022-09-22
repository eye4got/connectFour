from heuristicAI import HeuristicAI
import numpy as np

class TestHeuristicAI:

    def test_check_slot_for_consec_tokens_one(self):
        player = HeuristicAI(player_num = 1)
        board_arr = np.zeros(shape = (6, 7))
        board_arr[0, 4:] = 2
        coords = (0, 3)

        result = player._check_slot_for_consec_tokens(board_arr, coords, 2)

        assert result == 3

    def test_check_slot_for_consec_tokens_two(self):
        player = HeuristicAI(player_num = 1)
        board_arr = np.zeros(shape = (6, 7))
        board_arr[0][0] = 2
        board_arr[1][1] = 2
        board_arr[3][3] = 2
        coords = (2, 2)

        result = player._check_slot_for_consec_tokens(board_arr, coords, 2)

        assert result == 3

    def test_choose_move_blocking_one(self):
        player = HeuristicAI(player_num = 1)
        board_arr = np.zeros(shape = (6, 7))
        board_arr[:3, 0] = 2
        legal_moves = [x for x in range(1,8)]
        row_heights = [3] + [0] * 6
        chosen_move = player.choose_move(board_arr, legal_moves, row_heights)

        assert chosen_move == 1

    def test_choose_move_blocking_two(self):
        player = HeuristicAI(player_num = 1)
        board_arr = np.zeros(shape = (6, 7))
        board_arr[0][0] = 2
        board_arr[1][1] = 2
        board_arr[1][2] = 2
        board_arr[3][3] = 2
        board_arr[0][4] = 1
        legal_moves = [x for x in range(1,8)]
        row_heights = [1, 2, 2, 4, 1, 0, 0]
        chosen_move = player.choose_move(board_arr, legal_moves, row_heights)

        assert chosen_move == 3

    def test_choose_move_blocking_three(self):

        player = HeuristicAI(player_num = 1)
        board_arr = np.array([[2, 1, 1, 1, 2, 0, 0],
                              [0, 2, 1, 1, 1, 0, 0],
                              [0, 2, 2, 2, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]])

        legal_moves = [x for x in range(1, 8)]
        row_heights = [1, 3, 3, 4, 2, 0, 0]
        chosen_move = player.choose_move(board_arr, legal_moves, row_heights)

        assert chosen_move == 5

    def test_choose_move_avoid_enabling(self):

        player = HeuristicAI(player_num = 1)
        board_arr = np.array([[2, 2, 1, 1, 2, 2, 2],
                              [0, 2, 1, 1, 0, 2, 2],
                              [0, 0, 1, 1, 0, 0, 0],
                              [0, 0, 2, 2, 0, 0, 0],
                              [0, 0, 1, 1, 0, 0, 0],
                              [0, 0, 1, 1, 0, 0, 0]])

        legal_moves = [1, 2, 5, 6, 7]
        row_heights = [1, 2, 6, 6, 1, 2, 2]
        chosen_move = player.choose_move(board_arr, legal_moves, row_heights)

        assert chosen_move == 2