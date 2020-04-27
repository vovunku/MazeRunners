import lib.game_facade as game_facade
import lib.editor_facade as editor_facade


class MenuFacade:
    """Accelerate different modules of application"""

    def __init__(self, receiver, display, lib_path):
        self.receiver = receiver
        self.display = display
        self.editor_body = editor_facade.EditorFacade(receiver, display, lib_path)
        self.game_body = game_facade.GameFacade(receiver, display)
        self.running = False

    def start_main_loop(self):
        self.running = True
        self.display.menu()
        while self.running:
            inp = self.receiver.handle_string()
            if inp[0] == "1":
                self.display.message("Choose map")
                try:
                    game_map = self.editor_body.choose_map()
                except Exception as err:
                    self.display.message("Error: {0}".format(str(err)))
                    continue
                self.game_body.set_map(game_map)
                self.game_body.game_loop()
            elif inp[0] == "2":
                self.editor_body.edit_loop()
            elif inp[0] == "3":
                self.display.message("See you later!")
                self.running = False
            self.display.menu()
