import cProfile
import pstats
import random
from typing import Callable, Union, Optional
import logging
from heuristicAI import HeuristicAI

from random import choice

logging.basicConfig(filename = "results.log",
                    level = logging.INFO,
                    format = "%(asctime)s %(message)s")

from gameBoard import GameBoard

# TODO: unit tests

def run_simulation(player_one_move: Callable, player_two_move: Callable) -> GameBoard:

    board = GameBoard()

    while board.is_complete is False:
        board.add_piece(player_one_move(board.board, board.legal_moves, board.row_heights))

        if not board.is_complete:
            board.add_piece(player_two_move(board))

    return board

player_one = HeuristicAI(player_num=1)

def player_two_move_choice(board: GameBoard):

    move = choice(board.legal_moves)

    return move

num_sims = 1000000
stalemates = 0
player_wins = [0, 0]

# TODO: Clean up main and wrap in function?
with cProfile.Profile() as pr:
    for ii in range(num_sims):
        logging.info(f"\n\nStart Game: {ii + 1}  " + "*" * 30)
        curr_board = run_simulation(player_one.choose_move, player_two_move_choice)

        if curr_board.victor is None:
            stalemates += 1

        else:
            player_wins[curr_board.victor - 1] += 1

        if ii % 10000 == 0:
            logging.warning(f"Games: {ii + 1}")
            print(f"Player One Wins: {player_wins[0]}")
            print(f"Player Two Wins: {player_wins[1]}")
            print(f"Stalemates: {stalemates}\n")

stats = pstats.Stats(pr)
stats.dump_stats(filename="performance_profile.prof")

print(f"Player One Wins: {player_wins[0]}")
print(f"Player Two Wins: {player_wins[1]}")
print(f"Stalemates: {stalemates}")