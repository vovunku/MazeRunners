from abc import ABC, abstractmethod
import lib.command as command


class DestinationStrategy:
    """To avoid copypasta(strategy pattern)"""

    @abstractmethod
    def cell_move(self, cell, user_id):
        pass

    @abstractmethod
    def player_move(self, player):
        pass

    @abstractmethod
    def next_cell(self, cell):
        pass


class ActLeft(DestinationStrategy):
    def __init__(self):
        self.type = "LEFT"

    def cell_move(self, cell, user_id):
        if cell.left is None:
            return [command.WallStopCommand(cell, self)]
        command_list = cell.left.activate()
        command_list.insert(0, command.MoveCommand(cell, self))
        return command_list

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y - 1)

    def next_cell(self, cell):
        return cell.left


class ActRight(DestinationStrategy):
    def __init__(self):
        self.type = "RIGHT"

    def cell_move(self, cell, user_id):
        if cell.right is None:
            return [command.WallStopCommand(cell, self)]
        command_list = cell.right.activate()
        command_list.insert(0, command.MoveCommand(cell, self))
        return command_list

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y + 1)

    def next_cell(self, cell):
        return cell.right


class ActUp(DestinationStrategy):
    def __init__(self):
        self.type = "UP"

    def cell_move(self, cell, user_id):
        if cell.up is None:
            return [command.WallStopCommand(cell, self)]
        command_list = cell.up.activate()
        command_list.insert(0, command.MoveCommand(cell, self))
        return command_list

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x - 1, y)

    def next_cell(self, cell):
        return cell.up


class ActDown(DestinationStrategy):
    def __init__(self):
        self.type = "DOWN"

    def cell_move(self, cell, user_id):
        if cell.down is None:
            return [command.WallStopCommand(cell, self)]
        command_list = cell.down.activate()
        command_list.insert(0, command.MoveCommand(cell, self))
        return command_list

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x + 1, y)

    def next_cell(self, cell):
        return cell.down
