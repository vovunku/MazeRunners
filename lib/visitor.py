class GameVisitor:
    """Handle commands in game_loop"""

    def __init__(self, display, game):
        self.display = display
        self.game = game
        self.game_running = True
        self.turn_running = True
        self.player = None

    def set_player(self, player):
        self.player = player

    def visit_stun_c(self, command):
        self.display.message(
            "{0} has been stunned for {1} turns".format(self.player.id, command.stun_duration))
        command.execute(self.player)

    def visit_armory_c(self, command):
        self.display.message(
            "{0} bullets has been restored({1})".format(self.player.id, command.ammunition))
        command.execute(self.player)

    def visit_teleport_c(self, command):
        self.display.message(
            "{0} has been teleported".format(self.player.id))
        command.execute(self.player)

    def visit_exit_c(self, command):
        self.display.message(
            "{0} succeeded! End of game!".format(self.player.id))
        command.execute(self.player)
        self.turn_running = False
        self.game_running = False

    def visit_move_c(self, command):
        self.display.message(
            "{0} successfully moved {1}".format(self.player.id, command.move_strategy.type.lower()))
        if command.type == "RubberRoom":
            self.display.message("{0} successfully exited Rubber Room".format(self.player.id))
        command.execute(self.player)

    def visit_false_move_c(self, command):
        self.display.message(
            "{0} successfully moved {1}".format(self.player.id, command.move_strategy.type.lower()))
        command.execute(self.player)

    def visit_wall_stop_c(self, command):
        self.display.message(
            "{0} didn't move {1} because of wall".format(self.player.id, command.move_strategy.type.lower()))
        command.execute(self.player)

    def visit_i_move_c(self, command):
        command.execute(self.game, self.player.id)

    def visit_i_shoot_c(self, command):
        command.execute(self.game, self.player.id)

    def visit_i_help_c(self, command):
        self.display.help()
        command.execute(self.player)

    def visit_respawn_c(self, command):
        self.display.message("{0} has been respawned".format(self.player.id))
        command.execute(self.game, self.player.id)

    def visit_death_c(self, command):
        self.display.message("{0} has died".format(self.player.id))
        command.execute(self.player)

    def visit_bad_action_move_c(self, command):
        self.display.message("{0}: bad action; type - {1}".format(self.player.id, command.type))
        command.execute(self.player)

    def visit_i_backpack_c(self, command):
        result = command.execute(self.player)
        self.display.message("here your backpack")
        for item, val in result.items():
            self.display.message("{0}: {1}".format(item, val))

    def visit_start_turn_c(self, command):
        command.execute(self.player)

    def visit_end_turn_c(self, command):
        self.display.message("{0} turn ended".format(self.player.id))
        self.turn_running = False
        command.execute(self.player)

    def visit_stun_skip_c(self, command):
        remain = command.execute(self.player)
        self.display.message("You skip turn! {0} turns to skip remain!".format(remain))

    def visit_nice_shoot_c(self, command):
        self.display.message("Nice shoot! You have shot {0}".format(command.aim_id))
        command.execute(self.player)

    def visit_bad_shoot_c(self, command):
        self.display.message("Unfortunately you missed")
        command.execute(self.player)
