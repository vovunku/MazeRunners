from abc import ABC, abstractmethod


class CellCommand(ABC):
    """Interface for commands from cells to player"""

    def __init__(self, cell):
        self.cell = cell

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def execute(self, player):
        pass


class StunCommand(CellCommand):
    """Command from Stun cell by stunning"""

    def accept(self, visitor):
        visitor.visit_stun_c(self)

    def execute(self, player):
        player.stun(self.cell.stun_duration)


class ArmoryCommand(CellCommand):
    """Command from Armory cell by fulling ammo"""

    def accept(self, visitor):
        visitor.visit_armory_c(self)

    def execute(self, player):
        player.receive_ammo(self.cell.ammunition)


class TeleportCommand(CellCommand):
    """Command from Teleport cell"""

    def accept(self, visitor):
        visitor.visit_teleport_c(self)

    def execute(self, player):
        end_cell = self.cell.shift_destination
        player.set_coords(end_cell.lay, end_cell.x, end_cell.y)


class ExitCommand(CellCommand):
    """Command from Exit cell by exiting"""

    def accept(self, visitor):
        visitor.visit_exit_c(self)

    def execute(self, player):
        pass


class MoveCommand(CellCommand):
    """Command for standard move"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_move_c(self)

    def execute(self, player):
        self.move_strategy.player_move(player)
        player.move_count -= 1


class FalseMoveCommand(CellCommand):
    """Command for false moving in rubber room"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_false_move_c(self)

    def execute(self, player):
        player.move_count -= 1


class WallStopCommand(CellCommand):
    """Command for player unable to move"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_wall_stop_c(self)

    def execute(self, player):
        pass


class DeathCommand(CellCommand):
    """Command for player got killed"""

    def accept(self, visitor):
        visitor.visit_death_c(self)

    def execute(self, player):
        player.respawn()


# ======================================================================================================================


class BoardCommand(ABC):
    """Interface for commands from user to player"""

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def execute(self, board, player):
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


class InputHelpCommand(BoardCommand):  # вероятно нужно перенести куда-то еще, тк не вписывается в общую логику
    """Command from user for help display"""

    def accept(self, visitor):
        visitor.visit_i_help_c(self)

    def execute(self, board, player_id):
        pass


class InputEndTurnCommand(BoardCommand):
    def accept(self, visitor):
        visitor.visit_i_end_turn_c(self)

    def execute(self, board, player_id):
        board.reset(player_id)


class RespawnCommand(BoardCommand):
    def accept(self, visitor):
        visitor.visit_respawn_c(self)

    def execute(self, board, player_id):
        board.respawn(player_id)


# ======================================================================================================================


class EventCommand(ABC):

    @abstractmethod
    def accept(self, visitor):
        pass

    def execute(self):
        pass


class BadActionCommand(EventCommand):
    """Command for undone action"""

    def __init__(self, type):
        self.type = type

    def accept(self, visitor):
        visitor.visit_bad_action_move_c(self)
