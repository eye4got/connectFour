import logging
import numpy as np
import numpy.typing as npt
from typing import Union, Tuple, List

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

class Player:

    def __init__(self, token: int):
        self.token = token

    def select_move(self, board: np.ndarray[2]) -> int:
        pass

