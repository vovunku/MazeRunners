import queue


class Player:
    """Simplest player"""

    def __int__(self, lay, x, y, player_id, global_statements):
        self.type = "Base"
        self.backpack = {"Ammo": 0}
        self.statement = {"Stun": 0}
        self.coords = {"Lay": lay, "X": x, "Y": y}
        self.id = player_id
        self.command_log = []
        self.command_queue = queue.Queue()

    def check_backpack(self):
        return self.backpack

    def check_statement(self):
        return self.statement

    def stun(self, duration):
        self.statement[duration] = duration

    def receive_ammo(self, ammunition):
        self.backpack["Ammo"] = max(self.backpack["Ammo"], ammunition)

    def handle_command(self, command):
        self.command_log.append(command)
        self.command_queue.put(command)

    def set_coords(self, lay, x, y):
        self.coords["Lay"] = lay
        self.coords["X"] = x
        self.coords["Y"] = y

    def get_coords(self):
        return self.coords
