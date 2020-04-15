from abc import ABC, abstractmethod


class PlayerCommand(ABC):
    """Interface for commands from different objects to player"""

    @abstractmethod
    def execute(self, player):
        pass


class StunCommand(PlayerCommand):
    """Command from Stun cell by stunning"""

    def __init__(self, cell):
        self.cell = cell

    def execute(self, player):
        player.stun(self.cell.duration)


class ArmoryCommand(PlayerCommand):
    """Command from Armory cell by fulling ammo"""

    def __init__(self, cell):
        self.cell = cell

    def execute(self, player):
        player.receive_ammo(self.cell.ammunition)


class TeleportCommand(PlayerCommand):
    """Command from Teleport cell"""

    def __init__(self, cell):
        self.cell = cell

    def execute(self, player):
        end_cell = self.cell.shift_destination
        player.set_coords(end_cell.lay, end_cell.x, end_cell.y)


class ExitCommand(PlayerCommand):
    """Command from Exit cell by exiting"""

    def __init__(self, cell):
        self.cell = cell

    def execute(self, player):
        player.achieve_exit()
