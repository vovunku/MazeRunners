from abc import ABC, abstractmethod


class Handler(ABC):
    """Handler interface"""

    def set_next(self, next_handler):
        pass

    def handle(self, request):
        pass

class ActivatingHandler(Handler):
    """Handle shoots/objects activating"""

    def __init__(self, board, receiver, display, players, user_id):
        self.board = board
        self.receiver = receiver
        self.display = display
        self.players = players
        self.user_id = user_id
        self.next_handler = None

    def set_next(self, next_handler):
        self.next_handler = next_handler

    def handle(self, request):
        self.display.message("Action phase(to skip - write end)")
        while True:
            inp = self.receiver.handle_command()
            if inp == "help":
                self.display.help()
            elif inp == "backpack":
                self.display
            if "shoot" in inp:

