import lib.command as command


class Cell:
    def __init__(self, items=None, **kwargs):
        self.items = items or []
        self.set_neighbour(**kwargs)
        self.storage = []
        self.set_coords(kwargs.get("lay", 0), kwargs.get("x", 0), kwargs.get("y", 0))
        self.players = set()

    def activate_on_step(self):
        return []

    def collect(self):
        tmp = self.storage
        self.storage = []
        return tmp

    def observe(self):
        return tuple(self.storage)

    def put_in(self, *args):
        self.storage.extend(args)

    def move(self, player_id, move_strategy):
        return move_strategy.cell_move(self, player_id)

    def set_neighbour(self, **kwargs):
        self.left = kwargs.get("LEFT")
        self.right = kwargs.get("RIGHT")
        self.up = kwargs.get("UP")
        self.down = kwargs.get("DOWN")

    def set_coords(self, lay, x, y):
        self.lay = lay
        self.x = x
        self.y = y

    def get_coord(self):
        return [self.lay, self.x, self.y]

    def get_accessible(self):
        ans = [dest for dest in [self.left, self.right, self.up, self.down] if dest is not None]
        return ans

    def release_player(self, player_id):
        self.players.remove(player_id)

    def handle_player(self, player_id):
        self.players.add(player_id)


class Empty(Cell):
    def __init__(self):
        super().__init__()


class Stun(Cell):
    def __init__(self, stun_duration, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.stun_duration = stun_duration

    def activate_on_step(self):
        return [command.StunCommand(self.stun_duration)]


class RubberRoom(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.exit_destination = exit_destination

    def move(self, player_id, move_strategy):
        if move_strategy.destination_type == self.exit_destination:
            return move_strategy.cell_move(self, player_id)
        return [command.FalseMoveCommand(move_strategy)]

    def get_accessible(self):
        for neighbour_cell, it_exit_destination in zip([self.left, self.right, self.up, self.down], ["LEFT", "RIGHT", "UP", "DOWN"]):
            if neighbour_cell is not None and self.exit_destination == it_exit_destination:
                return [neighbour_cell]
        return []


class Teleport(Cell):
    def __init__(self, shift_lay, shift_x, shift_y, shift_destination=None, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.shift_destination = shift_destination
        self.shift_lay = shift_lay
        self.shift_x = shift_x
        self.shift_y = shift_y

    def get_accessible(self):
        ans = [self.shift_destination]
        return ans

    def set_shift_destination(self, shift_destination):
        self.shift_destination = shift_destination

    def activate_on_step(self):
        while self.players:
            player_id = self.players.pop()
            self.shift_destination.handle_player(player_id)
        lay = self.shift_destination.lay
        x = self.shift_destination.x
        y = self.shift_destination.y
        return [command.TeleportCommand(lay, x, y)]


class Armory(Cell):
    def __init__(self, ammunition=3, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.ammunition = ammunition

    def activate_on_step(self):
        return [command.ArmoryCommand(self.ammunition)]


class Exit(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.exit_destination = exit_destination

    def move(self, player_id, move_strategy):
        if move_strategy.destination_type == self.exit_destination:
            self.release_player(player_id)
            return [command.ExitCommand()]
        return super().move(player_id, move_strategy)
