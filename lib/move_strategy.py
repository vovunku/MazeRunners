from abc import ABC, abstractmethod
import lib.command as command


class DestinationStrategy:
    """To avoid copypasta(strategy pattern)"""

    def cell_move(self, cell, user_id):
        next_cell = self.next_cell(cell)
        if next_cell is None:
            return [command.WallStopCommand(self)]
        cell.release_player(user_id)
        next_cell.handle_player(user_id)
        command_list = next_cell.activate()
        command_list.insert(0, command.MoveCommand(cell.type, self))
        return command_list

    @abstractmethod
    def player_move(self, player):
        pass

    @abstractmethod
    def next_cell(self, cell):
        pass


class ActLeft(DestinationStrategy):
    def __init__(self):
        self.type = "LEFT"

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y - 1)

    def next_cell(self, cell):
        return cell.left


class ActRight(DestinationStrategy):
    def __init__(self):
        self.type = "RIGHT"

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y + 1)

    def next_cell(self, cell):
        return cell.right


class ActUp(DestinationStrategy):
    def __init__(self):
        self.type = "UP"

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x - 1, y)

    def next_cell(self, cell):
        return cell.up


class ActDown(DestinationStrategy):
    def __init__(self):
        self.type = "DOWN"

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x + 1, y)

    def next_cell(self, cell):
        return cell.down
