import cProfile
import pstats
import random
from typing import Callable, Union, Optional
import logging

from random import choice

logging.basicConfig(filename = "results.log",
                    level = logging.WARNING,
                    format = "%(asctime)s %(message)s")

from gameBoard import GameBoard

# TODO: benchmarking to improve performance
# TODO: unit tests
# TODO: setup Git

def run_simulation(player_one_move: Callable[[GameBoard], int], player_two_move: Callable[[GameBoard], int]) -> GameBoard:

    board = GameBoard()

    while board.is_complete is False:
        move = player_one_move(board)
        board.add_piece(move)

        if not board.is_complete:
            move = player_two_move(board)
            board.add_piece(move)

    return board

def player_one_move_choice(board: GameBoard):

    move = choice(board.legal_moves)

    # TODO: check if there is a victorious move
    # TODO: check if there is a blocking move

    # TODO: Add logging and try/except block to AI in case of illegal move

    return move

def player_two_move_choice(board: GameBoard):

    move = choice(board.legal_moves)

    return move

num_sims = 300000
stalemates = 0
player_wins = [0, 0]

# TODO: Clean up main and wrap in function?
with cProfile.Profile() as pr:
    for ii in range(num_sims):
        logging.info(f"\n\nStart Game: {ii + 1}  " + "*" * 30)
        curr_board = run_simulation(player_one_move_choice, player_two_move_choice)

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

