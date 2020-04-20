class GameVisitor:
    """Handle commands in game_loop"""

    def __init__(self, display, board):
        self.display = display
        self.board = board
        self.game_running = True
        self.turn_running = True
        self.player = None

    def set_player(self, player):
        self.player = player

    def visit_stun_c(self, command):
        self.display.message(
            "{0} player has been stunned for {1} turns"
            .format(self.player.id, command.cell.duration))
        #  не очень хорошо так далеко залезать, мб лучше передавать в команду только необходимую инфу
        #  кажись закон деметры нарушается, но пока так
        command.execute(self.player)

    def visit_armory_c(self, command):
        self.display.message(
            "{0} player bullets has been restored({1})"
            .format(self.player.id, command.cell.ammunition))
        command.execute(self.player)

    def visit_teleport_c(self, command):
        self.display.message(
            "{0} player has been teleported"
            .format(self.player.id))
        command.execute(self.player)

    def visit_exit_c(self, command):
        self.display.message(
            "{0} player succeeded! End of game!"
            .format(self.player.id))
        command.execute(self.player)
        self.turn_running = False
        self.game_running = False

    def visit_move_c(self, command):
        self.display.message(
            "{0} player successfully moved {1}"
            .format(self.player.id, command.move_strategy.type.lowercase()))
        command.execute(self.player)

    def visit_false_move_c(self, command):
        self.display.message(
            "{0} player successfully moved {1}"
            .format(self.player.id, command.move_strategy.type.lowercase()))
        command.excute()

    def visit_wall_stop_c(self, command):
        self.display.message(
            "{0} player didn't move {1} because of wall"
            .format(self.player, command.move_strategy.type.lowercase()))
        command.execute(self.player)

    def visit_i_move_c(self, command):
        command.execute(self.board, self.player.id)

    def visit_i_shoot_c(self, command):
        command.execute(self.board, self.player.id)

    def visit_i_help_c(self, command):
        self.display.help()
        command.execute(self.board, self.player.id)

    def visit_i_end_turn_c(self, command):
        self.turn_running = False
        command.execute(self.board, self.player.id)
