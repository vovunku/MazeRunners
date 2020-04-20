from abc import ABC, abstractmethod
from shutil import copy
import os


class MapManager(ABC):
    """Interface for map storage"""

    @abstractmethod
    def get_map_list(self):
        pass

    @abstractmethod
    def get_map(self, map_id):
        pass

    @abstractmethod
    def add_map_file(self, filename):
        pass


class ConsoleMapManager(MapManager):
    """Simpliest implementation"""

    def __init__(self, lib_path):
        self.lib_path = lib_path
        self.map_list = []
        with os.scandir(self.lib_path) as maps:
            for game_map in maps:
                abs_path = game_map.path
                related_path = abs_path[len(self.lib_path):]
                self.map_list.append(related_path)

    def get_map_list(self):
        return self.map_list

    def get_map(self, map_id):
        return self.lib_path + self.map_list[map_id]

    def add_map_file(self, filename):
        copy(filename, self.lib_path)
