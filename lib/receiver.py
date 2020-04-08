from __future__ import annotations
from abc import ABC, abstractmethod
import typing
import sys


class Receiver(ABC):
    """Receiver interface"""

    def __int__(self):
        self.type = "Abstract"

    @abstractmethod
    def handle_string(self):
        pass


class SimpleConsoleReceiver(Receiver):
    """Console receiver with only text input (no keys supported)"""

    def __int__(self):
        self.type = "Console"

    def handle_string(self) -> typing.List[str, ...]:
        inp = sys.stdin.readline().strip()
        return tuple(inp.split(" "))
