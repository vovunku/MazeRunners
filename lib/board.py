import cell


class Board:
    """Incapsulate cell storage and move initialisation"""

    def __init__(self, board, player_dict):
        self.storage = board
        self.player_dict = player_dict