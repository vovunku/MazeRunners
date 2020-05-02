import lib.player as player
import lib.visitor as visitor
import lib.board as board


class GameFacade:
    """Accelerate game modules and allow interaction"""

    def __init__(self, receiver, display):
        self.receiver = receiver
        self.display = display
        self.board = None
        self.players = None
        self.game_map = None

    def game_loop(self):
        self.initialize()
        game_visitor = visitor.GameVisitor(self.display, self.board)
        self.display.help()
        while game_visitor.game_running:
            for player_id, player in self.players.items():
                if not game_visitor.game_running:
                    break
                self.display.message("{0} player turn started".format(player_id))
                game_visitor.set_player(player)
                self.board.start_turn(player_id)
                order_queue = player.command_queue
                game_visitor.turn_running = True
                while game_visitor.turn_running:
                    while not order_queue.empty() and game_visitor.turn_running:
                        next_command = order_queue.get()
                        next_command.accept(game_visitor)
                    if game_visitor.turn_running and order_queue.empty():
                        incorrect = True
                        while incorrect:
                            try:
                                new_command = self.receiver.handle_game_command()
                                player.handle_command_list([new_command])
                                incorrect = False
                            except Exception as err:
                                self.display.message("Error: {0}".format(str(err)))

    def initialize(self):
        if self.game_map is None:
            raise ValueError("No map provided")
        self.display.message("Insert players information")
        self.display.message("Insert players quantity")
        start_info = self.receiver.handle_string()
        n = int(start_info[0])
        players = dict()
        for p_id in range(n):
            self.display.message("Insert spawn position of player {0}".format(
                p_id + 1))  # TODO контектстный менеджер на обработку ошибок
            self.display.message("input format: <Name> <lay> <x> <y>")
            player_name, spawn_lay, spawn_x, spawn_y = self.receiver.handle_string()
            if player_name in players:
                raise ValueError("such player already exist")
            spawn_lay = int(spawn_lay) - 1
            spawn_x = int(spawn_x) - 1
            spawn_y = int(spawn_y) - 1
            players[player_name] = player.Player(spawn_lay, spawn_x, spawn_y, spawn_lay, spawn_x, spawn_y, player_name)
        self.players = players
        self.board = board.Board(self.game_map, players)

    def set_map(self, game_map):
        self.game_map = game_map
