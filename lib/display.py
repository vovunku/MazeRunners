from abc import ABC, abstractmethod
import os


class Display(ABC):
    """Display interface"""

    def __init__(self):
        self.type = "Abstract"

    @abstractmethod
    def menu(self):
        pass

    @abstractmethod
    def message(self, message: str):
        pass


class ConsoleDisplay(Display):
    """Simplest Console Display"""

    def __init__(self):
        super().__init__()
        self.type = "Console"

    def clear_row(self):
        if 'posix' in os.name:  # Clear the Linux terminal.
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):  # Clear Windows command prompt.
            os.system('cls')

    def menu(self):
        print("{:=^80}".format("Welcome to MazeRunners!"))
        print("{:<80}".format("1 Play"))
        print("{:<80}".format("2 Add map"))
        print("{:<80}".format("3 Exit"))

    def message(self, message: str):
        print("{0:^80}".format(message))

    def help(self):
        print("{:<80".format("DESTINATION - {LEFT, RIGHT, UP, DOWN"))
        print("{:<80".format("to shoot - shoot DESTINATION"))
        print("{:<80".format("to move - move DESTINATION"))
        print("{:<80".format("to check backpack - backpack"))
        print("{:<80".format("to check statement - statement"))
        print("{:<80".format("to end phase - end"))
