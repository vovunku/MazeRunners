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

    def menu(self):
        print("{:=^80}".format("Welcome to MazeRunners!"))
        print("{:<80}".format("1 Play"))
        print("{:<80}".format("2 Add map"))
        print("{:<80}".format("3 Exit"))

    def message(self, message: str):
        print("{0:<80}".format(message))

    def help(self):
        print("{:<80}".format("DESTINATION - {LEFT, RIGHT, UP, DOWN}"))
        print("{:<80}".format("to shoot type - \"shoot\" <DESTINATION>"))
        print("{:<80}".format("to move - \"move\" <DESTINATION>"))
        print("{:<80}".format("to check backpack - \"backpack\""))
        print("{:<80}".format("to see help - \"help\""))

    def map_list(self, map_list):
        for id, game in enumerate(map_list):
            print("{0} {1:<80}".format(id + 1, game))
