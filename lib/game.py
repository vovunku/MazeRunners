import lib.command as command


class Game:
    """Incapsulate cell storage and move initialisation"""

    def __init__(self, game_map, player_dict):
        self.game_map = game_map
        self.player_dict = player_dict
        for player_id in player_dict:
            self.respawn(player_id)

    def move(self, player_id, move_strategy):
        player = self.player_dict[player_id]
        if player.action_points <= 0 or player.statement["Stun"] > 0:
            player.handle_command_list([command.BadActionCommand("move")])
            return None
        lay, x, y = player.get_coords()
        cell = self.game_map[lay][x][y]
        command_list = cell.move(player_id, move_strategy)
        player.handle_command_list(command_list)

    def end_of_turn(self, player_id):
        player = self.player_dict[player_id]
        player.end_of_turn()

    def shoot(self, player_id, shoot_strategy):
        player = self.player_dict[player_id]
        if player.backpack["Ammo"] == 0 or player.action_points <= 0:
            player.handle_command_list([command.BadActionCommand("shoot")])
            return None
        player.backpack["Ammo"] -= 1
        lay, x, y = player.get_coords()
        cur_cell = self.game_map[lay][x][y]
        while cur_cell:
            player_pool = cur_cell.players.difference({player_id})
            if player_pool:
                killed_player = player_pool.pop()
                cur_cell.players.remove(killed_player)
                self.player_dict[killed_player].handle_command_list(
                    [command.DeathCommand(), command.RespawnCommand()])
                self.player_dict[player_id].handle_command_list([command.NiceShootCommand(killed_player)])
                break
            cur_cell = shoot_strategy.next_cell(cur_cell)
        else:
            self.player_dict[player_id].handle_command_list([command.BadShootCommand()])

    def respawn(self, player_id):
        player = self.player_dict[player_id]
        lay, x, y = player.get_coords()
        self.game_map[lay][x][y].players.add(player_id)

    def start_turn(self, player_id):
        self.player_dict[player_id].handle_command_list([command.StartTurnCommand()])
