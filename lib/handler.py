from abc import ABC, abstractmethod


class Handler(ABC):
    """Handler interface"""

    @abstractmethod
    def set_next(self, next_handler):
        pass

    @abstractmethod
    def handle(self, player_id):
        pass


class BaseGameHandler(Handler):
    """For avoiding copypast in handle"""

    def __init__(self, executor, display, receiver, message):
        self.next_handler = None
        self.executor = executor
        self.player_id = None
        self.message = message
        self.display = display
        self.receiver = receiver

    def set_next(self, next_handler):
        self.next_handler = next_handler

    def handle(self, player_id):
        if self.next_handler:
            return self.next_handler.handle(player_id)
        return None


class AskingHandler(BaseGameHandler):
    """For user questions in 3 phase"""

    def handle(self, player_id):
        self.player_id = player_id
        self.display.message(self.message)
        while True:
            inp = self.receiver.handle_command()
            if "end" in set(inp):
                break
            if not self.executor.is_asking(inp):
                if inp == "end":
                    break
                self.display.message("Incorrect input")
                #self.display.incorrect_input()
        super().handle(inp)


class ActHandler(BaseGameHandler):
    """Activate move/shoot"""

    def handle(self, player_id):
        self.player_id = player_id
        self.display.message(self.message)
        move_count = 1
        while True:
            inp = self.receiver.handle_command()
            if self.executor.is_asking(inp):
                pass
            elif "move" in set(inp) and move_count > 0:
                self.executor.move_player(self.player_id, inp[1])
            elif "shoot" in set(inp):
                self.executor.move_player(self.player_id, inp[1])
            elif "end" in set(inp):
                break
            else:
                self.display.message("Incorrect input")
        super().handle(inp)


class ActivateHandler(BaseGameHandler):
    """Activate collect/..."""

    def handle(self, player_id):
        self.player_id = player_id
        self.display.message(self.message)
        while True:
            inp = self.receiver.handle_command()
            if self.executor.is_asking(inp):
                pass
            elif "collect" in set(inp):
                self.executor.collect_for_player(self.player_id)
            elif "end" in set(inp):
                break
            else:
                self.display.message("Incorrect input")
        super().handle(inp)

