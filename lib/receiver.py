from abc import ABC, abstractmethod
import sys


class Receiver(ABC):
    """Receiver interface"""

    def __int__(self):
        self.type = "Abstract"

    @abstractmethod
    def handle_command(self):
        pass

    @abstractmethod
    def read_map_file(self, filename):
        pass


class SimpleConsoleReceiver(Receiver):
    """Console receiver with only text input (no keys supported)"""

    def __int__(self):
        self.type = "Console"

    def handle_command(self):
        inp = sys.stdin.readline().strip()
        return list(inp.split(" "))

    def read_map_file(self, filename):
        ans_map = []
        with open(filename, 'r') as file:
            for line in file:
                ans_map.append(line.strip())
        return ans_map
