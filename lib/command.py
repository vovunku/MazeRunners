from abc import ABC, abstractmethod


class EnvCommand(ABC):
    """Interface for commands from cells to player"""

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def execute(self, player):
        pass


class StunCommand(EnvCommand):
    """Command from Stun cell by stunning"""

    def __init__(self, stun_duration):
        self.stun_duration = stun_duration

    def accept(self, visitor):
        visitor.visit_stun_c(self)

    def execute(self, player):
        player.stun(self.stun_duration)


class ArmoryCommand(EnvCommand):
    """Command from Armory cell by fulling ammo"""

    def __init__(self, ammunition):
        self.ammunition = ammunition

    def accept(self, visitor):
        visitor.visit_armory_c(self)

    def execute(self, player):
        player.receive_ammo(self.ammunition)


class TeleportCommand(EnvCommand):
    """Command from Teleport cell"""

    def __init__(self, d_lay, d_x, d_y):
        self.d_lay = d_lay
        self.d_x = d_x
        self.d_y = d_y

    def accept(self, visitor):
        visitor.visit_teleport_c(self)

    def execute(self, player):
        player.set_coords(self.d_lay, self.d_x, self.d_y)


class ExitCommand(EnvCommand):
    """Command from Exit cell by exiting"""

    def accept(self, visitor):
        visitor.visit_exit_c(self)

    def execute(self, player):
        pass


class MoveCommand(EnvCommand):
    """Command for standard move"""

    def __init__(self, type, move_strategy):
        self.type = type
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_move_c(self)

    def execute(self, player):
        self.move_strategy.player_move(player)
        player.spend_action()


class FalseMoveCommand(EnvCommand):
    """Command for false moving in rubber room"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_false_move_c(self)

    def execute(self, player):
        player.spend_action()


class WallStopCommand(EnvCommand):
    """Command for player unable to move"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_wall_stop_c(self)

    def execute(self, player):
        pass


class DeathCommand(EnvCommand):
    """Command for player got killed"""

    def accept(self, visitor):
        visitor.visit_death_c(self)

    def execute(self, player):
        player.respawn()


class InputBackpackCommand(EnvCommand):
    """Command to check backpack"""

    def accept(self, visitor):
        visitor.visit_i_backpack_c(self)

    def execute(self, player):
        return player.check_backpack()


class StartTurnCommand(EnvCommand):
    """Checks statement before turn starts"""

    def accept(self, visitor):
        visitor.visit_start_turn_c(self)

    def execute(self, player):
        player.start_turn()


class BadActionCommand(EnvCommand):
    """Command for undone action"""

    def __init__(self, type):
        self.type = type

    def accept(self, visitor):
        visitor.visit_bad_action_move_c(self)

    def execute(self, player):
        pass


class InputHelpCommand(EnvCommand):
    """Command from user for help display"""

    def accept(self, visitor):
        visitor.visit_i_help_c(self)

    def execute(self, player):
        pass


class EndTurnCommand(EnvCommand):
    """Interruption of turn"""

    def accept(self, visitor):
        visitor.visit_end_turn_c(self)

    def execute(self, player):
        player.end_of_turn()


class StunSkipCommand(EnvCommand):
    """Informing of skipping turn"""

    def accept(self, visitor):
        visitor.visit_stun_skip_c(self)

    def execute(self, player):
        return player.statement


class NiceShootCommand(EnvCommand):
    """Informing of nice shoot"""

    def __init__(self, dead_player_id):
        self.aim_id = dead_player_id

    def accept(self, visitor):
        visitor.visit_nice_shoot_c(self)

    def execute(self, player):
        player.spend_action()


class BadShootCommand(EnvCommand):
    """Informing of bad shoot"""

    def accept(self, visitor):
        visitor.visit_bad_shoot_c(self)

    def execute(self, player):
        player.spend_action()

# ======================================================================================================================


class BoardCommand(ABC):
    """Interface for commands from user to player"""

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def execute(self, board, player_id):
        pass


class InputMoveCommand(BoardCommand):
    """Command from user to move"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_i_move_c(self)

    def execute(self, board, player_id):
        board.move(player_id, self.move_strategy)


class InputShootCommand(BoardCommand):
    """Command for player shooting"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_i_shoot_c(self)

    def execute(self, board, player_id):
        board.shoot(player_id, self.move_strategy)


class RespawnCommand(BoardCommand):
    def accept(self, visitor):
        visitor.visit_respawn_c(self)

    def execute(self, board, player_id):
        board.respawn(player_id)
