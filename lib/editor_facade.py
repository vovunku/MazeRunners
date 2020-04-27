import lib.map_manager as map_manger
import lib.map_editor as map_editor


class EditorFacade:
    def __init__(self, receiver, display, lib_path):
        self.receiver = receiver
        self.display = display
        self.map_manager = map_manger.ConsoleMapManager(lib_path)
        self.map_editor = map_editor.MapEditor()

    def edit_loop(self):
        running = True
        self.display_help()
        while running:
            inp = self.receiver.handle_string()
            cmd_num = int(inp[0])
            if cmd_num == 1:
                self.check_map(inp[1])
            if cmd_num == 2:
                correct = self.check_map(inp[1])
                if correct:
                    self.add_map(inp[1])
                    self.display.message("Map added")
                else:
                    self.display.message("Map wasn\'t added")


    def choose_map(self):
        self.display.message("Please choose map from list. To choose - type the number of map in the list")
        map_list = self.map_manager.get_map_list()
        self.display.map_list(map_list)
        inp = self.receiver.handle_string()
        map_id = int(inp[0]) - 1
        if map_id >= len(map_list):
            raise KeyError("Incorrect number")
        map_path = self.map_manager.get_map(map_id)
        raw_map = self.map_manager.read_map_file(map_path)
        return self.map_editor.read_map(raw_map)

    def add_map(self, map_path):
        self.map_manager.add_map_file(map_path)

    def display_help(self):
        self.display.message("There are opportunities:")
        self.display.message("1 - Check map(you should provide path)")
        self.display.message("2 - Add map(also path needed)")
        self.display.message("To choose command, please, write: <number> <optional> <optional> ...")

    def check_map(self, filename):
        raw_map = self.map_manager.read_map_file(filename)
        game_map = self.map_editor.read_map(raw_map)
        try:
            result = self.map_editor.check_map(game_map)
            if result is None:
                self.display.message("Everything is correct!")
                return True
            else:
                self.display.message("Can't reach exit from this cell: {0}, {1}, {2}".format(result[0] + 1,
                                                                                     result[1] + 1,
                                                                                     result[2] + 1))
                return False
        except Exception as err:
            self.display.message("Error: {0}".format(str(err)))
            return False
