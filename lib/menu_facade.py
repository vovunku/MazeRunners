import lib.game_facade as game_facade


class MenuFacade:
    """Accelerate different modules of application"""

    def __init__(self, receiver, deploy, map_manager):
        self.receiver = receiver
        self.deploy = deploy
        self.map_manager = map_manager
        self.running = False

    def start_main_loop(self):
        self.running = True
        while self.running:
            self.deploy.menu()
            inp = self.receiver.handle_string()
            if inp[0] == "play":
                game_map = self.map_manager.choose_map()
                start_info = self.handle_string()
