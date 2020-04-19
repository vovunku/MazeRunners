import lib.handler as handler
import lib.receiver as receiver
import lib.display as display
import lib.map_editor as map_editor


class GameFacade:
    """Accelerate game modules and allow interaction"""

    def __init__(self, receiver, display, board, players_dict):
        self.receiver = receiver
        self.display = display
        self.board = board
        self.players = players_dict

    def game_loop(self):

