from shutil import copy
import os


class ConsoleMapManager:
    def __init__(self, lib_path):
        self.lib_path = lib_path
        self.map_list = []
        with os.scandir(self.lib_path) as maps:
            for game_map in maps:
                abs_path = game_map.path
                related_path = abs_path[len(self.lib_path):]
                self.map_list.append(related_path)

    def read_map_file(self, filename):
        ans_map = []
        with open(filename, 'r') as file:
            for line in file:
                ans_map.append(line.strip())
        return ans_map

    def get_map_list(self):
        return self.map_list

    def get_map(self, map_id):
        return self.lib_path + self.map_list[map_id]

    def add_map_file(self, filename):
        copy(filename, self.lib_path)
