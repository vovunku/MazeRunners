import lib.command as command


class Cell:
    def __init__(self, items=None, **kwargs):
        if items is None:
            self.items = []
        else:
            self.items = items
        self.type = "Base"
        self.left = kwargs.get("LEFT", None)
        self.right = kwargs.get("RIGHt", None)
        self.up = kwargs.get("UP", None)
        self.down = kwargs.get("DOWN", None)
        self.storage = []
        self.lay = kwargs.get("lay", 0)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.users = set()

    def activate(self, user):
        pass

    def collect(self):
        tmp = self.storage
        self.storage = []
        return tmp

    def observe(self):
        return tuple(self.storage)

    def put_in(self, *args):
        self.storage.extend(args)

    def move(self, move_strategy, player_id):
        return move_strategy.cell_move(self, player_id)

    def set_neighbour(self, **kwargs):
        self.left = kwargs.get("LEFT", None)
        self.right = kwargs.get("RIGHT", None)
        self.up = kwargs.get("UP", None)
        self.down = kwargs.get("DOWN", None)

    def __repr__(self):
        return self.type[:2]

    def set_coords(self, lay, x, y):
        self.lay = lay
        self.x = x
        self.y = y

    def get_coord(self):
        return [self.lay, self.x, self.y]

    def show_accessible(self):
        ans = []
        if self.left is not None:
            ans.append(self.left)
        if self.right is not None:
            ans.append(self.right)
        if self.up is not None:
            ans.append(self.up)
        if self.down is not None:
            ans.append(self.down)
        return ans


class Empty(Cell):
    def __init__(self):
        super().__init__()
        self.type = "Empty"


class Stun(Cell):
    def __init__(self, stun_duration, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.stun_duration = stun_duration
        self.type = "Stun"

    def activate(self, user):
        return command.StunCommand(self)


class RubberRoom(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.exit_destination = exit_destination
        self.type = "RubberRoom"

    def move(self, user_id, move_strategy):
        if move_strategy.type == self.exit_destination:
            return command.MoveCommand(move_strategy)
        return command.FalseMoveCommand(move_strategy)


class Teleport(Cell):
    def __init__(self, shift_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.shift_destination = shift_destination
        self.type = "Teleport"

    def show_accessible(self):
        ans = super().show_accessible()
        ans.append(self.shift_destination)
        return ans

    def set_shift_destination(self, shift_destination):
        self.shift_destination = shift_destination

    def activate(self, user):
        return (self.shift_destination.activate()).insert(0, command.TeleportCommand(self))


class Armory(Cell):
    def __init__(self, ammunition=3, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.type = "Armory"
        self.ammunition = ammunition

    def activate(self, user):
        return [command.ArmoryCommand(self.ammunition)]


class Exit(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        self.exit_destination = exit_destination
        self.type = "Exit"

    def move(self, user_id, move_strategy):
        if move_strategy.type == self.exit_destination:
            return command.ExitCommand(cell)
        return super().move()
