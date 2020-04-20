from abc import ABC, abstractmethod
import sys
import lib.move_strategy as strategy
import lib.command as command


class Receiver(ABC):
    """Receiver interface"""

    def __init__(self):
        self.type = "Abstract"

    @abstractmethod
    def handle_string(self):
        pass


class SimpleConsoleReceiver(Receiver):
    """Console receiver with only text input (no keys supported)"""

    def __init__(self):
        self.type = "Console"
        self.destinations = {"LEFT", "RIGHT", "UP", "DOWN"}

    def handle_string(self):
        inp = sys.stdin.readline().strip()
        return list(inp.split(" "))

    def create_strategy(self, key):
        if key == "LEFT":
            return strategy.ActLeft()
        elif key == "RIGHT":
            return strategy.ActRight()
        elif key == "UP":
            return strategy.ActUp()
        elif key == "DOWN":
            return strategy.ActDown()

    def handle_game_command(self):
        incorrect = True
        while incorrect:
            inp = self.handle_string()
            if inp[0] == "move":
                if inp[1] in self.destinations:
                    strat = self.create_strategy(inp[1])
                    return command.InputMoveCommand(strat)
            elif inp[0] == "shoot":
                if inp[1] in self.destinations:
                    strat = self.create_strategy(inp[1])
                    return command.InputShootCommand(strat)
            elif inp[0] == "end":
                return command.InputEndTurnCommand()
            elif inp[0] == "help":
                return command.InputHelpCommand()
