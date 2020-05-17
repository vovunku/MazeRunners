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
        command_list = next_cell.activate_on_step()
        command_list.insert(0, command.MoveCommand(type(cell), self))
        return command_list

    @abstractmethod
    def player_move(self, player):
        pass

    @abstractmethod
    def next_cell(self, cell):
        pass


class ActLeft(DestinationStrategy):

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y - 1)

    def next_cell(self, cell):
        return cell.left

    def __str__(self):
        return "LEFT"


class ActRight(DestinationStrategy):

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x, y + 1)

    def next_cell(self, cell):
        return cell.right

    def __str__(self):
        return "RIGHT"

class ActUp(DestinationStrategy):

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x - 1, y)

    def next_cell(self, cell):
        return cell.up

    def __str__(self):
        return "UP"

class ActDown(DestinationStrategy):

    def player_move(self, player):
        lay, x, y = player.get_coords()
        player.set_coords(lay, x + 1, y)

    def next_cell(self, cell):
        return cell.down

    def __str__(self):
        return "DOWN"
