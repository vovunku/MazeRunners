from abc import ABC, abstractmethod
import lib.command as command


class DestinationStrategy:
    """To avoid copypasta(strategy pattern)"""

    def __init__(self):
        self.destination_type = type(self).__name__.upper()

    def cell_move(self, cell, user_id):
        next_cell = self.next_cell(cell)
        if next_cell is None:
            return [command.WallStopCommand(self)]
        cell.release_player(user_id)
        next_cell.handle_player(user_id)
        command_list = next_cell.activate_on_step()
        command_list.insert(0, command.MoveCommand(type(cell), self))
        return command_list

    @abstractmethod
    def get_coord_diff(self):
        pass

    def player_move(self, player):
        x_diff, y_diff = self.get_coord_diff()
        lay, x, y = player.get_coords()
        player.set_coords(lay, x + x_diff, y + y_diff)

    def next_cell(self, cell):
        return getattr(cell, self.destination_type.lower())


class Left(DestinationStrategy):

    def get_coord_diff(self):
        return 0, -1


class Right(DestinationStrategy):

    def get_coord_diff(self):
        return 0, 1


class Up(DestinationStrategy):

    def get_coord_diff(self):
        return -1, 0


class Down(DestinationStrategy):

    def get_coord_diff(self):
        return 1, 0
