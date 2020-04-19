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
        return (cell.left.activate()).insert(0, command.MoveCommand(cell, self))

    def player_move(self, player):
        crd = player.get_coords()
        player.set_coords(crd["Lay"], crd["X"], crd["Y"] - 1)

    def next_cell(self, cell):
        return cell.left


class ActRight(DestinationStrategy):
    def __init__(self):
        self.type = "RIGHT"

    def cell_move(self, cell, user_id):
        if cell.right is None:
            return [command.WallStopCommand(cell, self)]
        return (cell.right.activate()).insert(0, command.MoveCommand(cell, self))

    def player_move(self, player):
        crd = player.get_coords()
        player.set_coords(crd["Lay"], crd["X"], crd["Y"] + 1)

    def next_cell(self, cell):
        return cell.right


class ActUp(DestinationStrategy):
    def __init__(self):
        self.type = "UP"

    def cell_move(self, cell, user_id):
        if cell.up is None:
            return [command.WallStopCommand(cell, self)]
        return (cell.up.activate()).insert(0, command.MoveCommand(cell, self))

    def player_move(self, player):
        crd = player.get_coords()
        player.set_coords(crd["Lay"], crd["X"] - 1, crd["Y"])

    def next_cell(self, cell):
        return cell.up


class ActDown(DestinationStrategy):
    def __init__(self):
        self.type = "DOWN"

    def cell_move(self, cell, user_id):
        if cell.down is None:
            return [command.WallStopCommand(cell, self)]
        return (cell.down.activate()).insert(0, command.MoveCommand(cell, self))

    def player_move(self, player):
        crd = player.get_coords()
        player.set_coords(crd["Lay"], crd["X"] + 1, crd["Y"])

    def next_cell(self, cell):
        return cell.down
