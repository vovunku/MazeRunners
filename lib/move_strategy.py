from abc import ABC, abstractmethod
import lib.command as command


class DirectionStrategy:
    """To avoid copypasta(strategy pattern)"""

    player_move_map = {
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
        "UP": (-1, 0),
        "DOWN": (1, 0)
    }

    cell_move_map = {
        "LEFT": "left",
        "RIGHT": "right",
        "UP": "up",
        "DOWN": "down"
    }

    def __init__(self, direction_type):
        self.direction_type = direction_type

    def cell_move(self, cell, user_id):
        next_cell = self.next_cell(cell)
        if next_cell is None:
            return [command.WallStopCommand(self)]
        cell.release_player(user_id)
        next_cell.handle_player(user_id)
        command_list = next_cell.activate_on_step()
        command_list.insert(0, command.MoveCommand(type(cell), self))
        return command_list

    def player_move(self, player):
        x_diff, y_diff = self.player_move_map[self.direction_type]
        lay, x, y = player.get_coords()
        player.set_coords(lay, x + x_diff, y + y_diff)

    def next_cell(self, cell):
        return getattr(cell, self.cell_move_map[self.direction_type])

