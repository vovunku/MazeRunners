from abc import ABC, abstractmethod
import sys
import lib.move_strategy as strategy
import lib.command as command


def create_strategy(key):
    return strategy.DirectionStrategy(key)


class Receiver(ABC):
    """Receiver interface"""

    @abstractmethod
    def handle_string(self):
        pass


class SimpleConsoleReceiver(Receiver):
    """Console receiver with only text input (no keys supported)"""

    def __init__(self):
        self.destinations = {"LEFT", "RIGHT", "UP", "DOWN"}

    def handle_string(self):
        inp = sys.stdin.readline().strip()
        return inp.split(" ")

    def handle_game_command(self):
        inp = self.handle_string()
        if inp[0] == "move":
            if inp[1] in self.destinations:
                strat = create_strategy(inp[1])
                return command.InputMoveCommand(strat)
            else:
                raise KeyError("Invalid input")
        elif inp[0] == "shoot":
            if inp[1] in self.destinations:
                strat = create_strategy(inp[1])
                return command.InputShootCommand(strat)
            else:
                raise KeyError("Invalid input")
        elif inp[0] == "help":
            return command.InputHelpCommand()
        elif inp[0] == "backpack":
            return command.InputBackpackCommand()
        else:
            raise KeyError("Invalid input")
