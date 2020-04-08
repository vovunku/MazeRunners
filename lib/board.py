from __future__ import annotations
import typing
import cell


class Board:
    """Incapsulate board storage and move initialisation"""

    def __init__(self,
                 board: typing.List[typing.List[typing.List[cell.Cell]]]):
        self._storage = board
