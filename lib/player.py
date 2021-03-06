from queue import Queue
import lib.command as command


class Player:
    """Simplest player"""

    def __init__(self, spawn_lay, spawn_x, spawn_y, lay, x, y, player_id):
        self.backpack = {"Ammo": 0}
        self.statement = {"Stun": 0}
        self.lay = lay
        self.x = x
        self.y = y
        self.id = player_id
        self.command_log = []
        self.command_queue = Queue()
        self.action_points = 1
        self.stun_points = 0
        self.spawn_lay = spawn_lay
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def check_backpack(self):
        return self.backpack

    def check_statement(self):
        return self.statement

    def stun(self, duration):
        self.statement["Stun"] = duration
        self.stun_points += duration

    def receive_ammo(self, ammunition):
        self.backpack["Ammo"] = max(self.backpack["Ammo"], ammunition)

    def handle_command_list(self, command_list):
        self.command_log = self.command_log + command_list
        for command in command_list:
            self.command_queue.put(command)

    def set_coords(self, lay, x, y):
        self.lay = lay
        self.x = x
        self.y = y

    def get_coords(self):
        return [self.lay, self.x, self.y]

    def end_of_turn(self):
        self.action_points = 1

    def spend_action(self):
        self.action_points -= 1
        if self.action_points == 0:
            self.handle_command_list([command.EndTurnCommand()])

    def respawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.lay = self.spawn_lay
        self.backpack["Ammo"] = 0
        self.statement["Stun"] = 0
        self.stun_points = 1
        self.action_points = 1

    def start_turn(self):
        if self.stun_points > 0:
            if self.statement["Stun"] > 0:
                self.statement["Stun"] -= 1
            self.stun_points -= 1
            self.handle_command_list([command.StunSkipCommand(), command.EndTurnCommand()])
