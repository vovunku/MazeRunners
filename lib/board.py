import lib. command as command


class Board:
    """Incapsulate cell storage and move initialisation"""

    def __init__(self, game_map, player_dict):
        self.game_map = game_map
        self.player_dict = player_dict

    def move(self, player_id, move_strategy):
        player = self.player_dict[player_id]
        if player.move_count == 0:
            player.handle_command_list([command.BadAction("move")])
            return None
        lay, x, y = player.get_coords()
        cell = self.game_map[lay][x][y]
        command_list = cell.move(player_id, move_strategy)
        player.handle_command_list(command_list)

    def reset(self, player_id):
        player = self.player_dict[player_id]
        player.reset()

    def shoot(self, player_id, shoot_strategy): # заглушка, по хорошему нужен класс с пулей
        player = self.player_dict[player_id]
        if player.backpack["Ammo"] == 0:
            player.move
        player.backpack["Ammo"] -= 1
        lay, x, y = player.get_coords()
        cur_cell = self.game_map[lay][x][y]
        while cur_cell:

