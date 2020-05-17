import unittest
import sys

sys.path.append('..')
import lib.cell as cell
import lib.move_strategy as move_strategy
import lib.command as command


class TestCellMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.cells = {
            "Empty": cell.Empty(),
            "Stun": cell.Stun(2),
            "Teleport": cell.Teleport(0, 0, 0, cell.Stun(2)),
            "Rubber": cell.RubberRoom("RIGHT"),
            "Exit": cell.Exit("UP"),
            "Armory": cell.Armory(3)
        }

        self.strategies = {
            "LEFT": move_strategy.Left(),
            "RIGHT": move_strategy.Right(),
            "UP": move_strategy.Up(),
            "DOWN": move_strategy.Down()
        }

        self.dummy_cells = {
            "LEFT": cell.Empty(),
            "RIGHT": cell.Empty(),
            "UP": cell.Empty(),
            "DOWN": cell.Empty()
        }

        self.respawn_test_unit()

    def respawn_test_unit(self):
        for test_cell in self.cells.values():
            test_cell.handle_player("test_unit")

    def set_dummy_neighbours(self):
        for test_cell in self.cells.values():
            test_cell.set_neighbour(LEFT=self.dummy_cells["LEFT"], RIGHT=self.dummy_cells["RIGHT"],
                                    UP=self.dummy_cells["UP"], DOWN=self.dummy_cells["DOWN"])

    def test_move_method(self):
        for strat_type, strat in self.strategies.items():
            for cell_type, test_cell in self.cells.items():
                if cell_type == "Rubber":
                    if strat_type != "RIGHT":
                        self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.FalseMoveCommand)
                    else:
                        self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.WallStopCommand)
                elif cell_type == "Exit" and strat_type == "UP":
                    self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.ExitCommand)
                else:
                    self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.WallStopCommand)
        self.set_dummy_neighbours()
        for strat_type, strat in self.strategies.items():
            self.respawn_test_unit()
            for cell_type, test_cell in self.cells.items():
                if cell_type == "Rubber" and strat_type != "RIGHT":
                    self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.FalseMoveCommand)
                elif cell_type == "Exit" and strat_type == "UP":
                    self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.ExitCommand)
                else:
                    self.assertIsInstance(test_cell.move("test_unit", strat)[0], command.MoveCommand)
        self.respawn_test_unit()


if __name__ == "__main__":
    unittest.main()
