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
        player.stun(self.cell.duration)


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
    """Command for standart move"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_move_c(self)

    def execute(self, player):
        self.move_strategy.player_move(player)


class FalseMoveCommand(CellCommand):
    """Command for false moving in rubber room"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_false_move_c(self)

    def execute(self, player):
        pass


class WallStopCommand(CellCommand):
    """Command for player unable to move"""

    def __init__(self, cell, move_strategy):
        super().__init__(cell)
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_wall_stop_c(self)

    def execute(self, player):
        pass
# ======================================================================================================================


class UserCommand(ABC):
    """Interface for commands from user to player"""

    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def execute(self, board, player):
        pass


class InputMoveCommand(UserCommand):
    """Command from user to move"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_i_move_c(self)

    def execute(self, board, player_id):
        board.move(player_id, self.move_strategy)


class InputShootCommand(UserCommand):
    """Command for player shooting"""

    def __init__(self, move_strategy):
        self.move_strategy = move_strategy

    def accept(self, visitor):
        visitor.visit_i_shoot_c(self)

    def execute(self, board, player_id):
        board.shoot(player_id, self.move_strategy)


class InputHelpCommand(UserCommand):
    def accept(self, visitor):
        visitor.visit_i_help_c(self)

    def execute(self, board, player_id):
        pass


class InputEndTurnCommand(UserCommand):
    def accept(self, visitor):
        visitor.visit_i_end_turn_c(self)

    def execute(self, board, player_id):
        board.reset(player_id)
