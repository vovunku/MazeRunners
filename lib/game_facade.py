import lib.receiver as receiver
import lib.display as display
import lib.map_editor as map_editor
import lib.visitor as visitor


class GameFacade:
    """Accelerate game modules and allow interaction"""

    def __init__(self, receiver, display, board, players_dict):
        self.receiver = receiver
        self.display = display
        self.board = board
        self.players = players_dict

    def game_loop(self):
        game_visitor = visitor.GameVisitor(self.display, self.board)
        while game_visitor.game_running:
            for player_id, player in self.players.items():
                self.display.help()
                if not game_visitor.game_running:
                    break
                self.display.message("{0} player turn started".format(player_id))
                game_visitor.set_player(player)
                order_queue = player.command_queue
                game_visitor.turn_running = True
                while game_visitor.turn_running:
                    while not order_queue.empty():
                        next_command = order_queue.get()
                        next_command.accept(game_visitor)
                    if game_visitor.turn_running and order_queue.empty():
                        new_command = self.receiver.handle_game_command()
                        player.handle_command_list([new_command])
