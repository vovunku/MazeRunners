import game_facade


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
            inp = self.receiver.handle_command()
            if inp in {1, "Play"}:

