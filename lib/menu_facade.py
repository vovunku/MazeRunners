import lib.game_facade as game_facade
import lib.player as player
import lib.board as board


class MenuFacade:
    """Accelerate different modules of application"""

    def __init__(self, receiver, display, map_editor):
        self.receiver = receiver
        self.display = display
        self.map_editor = map_editor
        self.running = False

    def start_main_loop(self):
        self.running = True
        while self.running:
            self.display.menu()
            inp = self.receiver.handle_string()
            if inp[0] == "Play":
                game_map = self.map_editor.choose_map()
                self.display.message("Insert players information")
                start_info = self.receiver.handle_string()
                n = int(start_info[0])
                players = dict()
                for p_id in range(n):
                    spawn_lay, spawn_x, spawn_y = map(int, self.receiver.handle_string())
                    spawn_lay -= 1
                    spawn_x -= 1
                    spawn_y -= 1
                    players[p_id] = player.Player(spawn_lay, spawn_x, spawn_y, spawn_lay, spawn_x, spawn_y, p_id)
                game_board = board.Board(game_map, players)
                game_body = game_facade.GameFacade(self.receiver, self.display, game_board, players)
                game_body.game_loop()
            elif inp[0] == "Add":
                self.display.message("Enter map path:")
                map_path = self.receiver.handle_string()[0]
                result = self.map_editor.check_map(map_path)
                if result:
                    self.display("Map is incorrect - problem cell = {0}".format(result))
                    continue
                self.map_editor.add_map(map_path)
            elif inp[0] == "End":
                self.display("See you later!")
                running = False
