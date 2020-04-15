class Cell:
    def __init__(self, items=None, **kwargs):
        if items is None:
            items = []
        self.left = kwargs.get("left", None)
        self.right = kwargs.get("right", None)
        self.up = kwargs.get("up", None)
        self.down = kwargs.get("down", None)
        self._storage = []
        self.lay = kwargs.get("lay", 0)
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)

    def activate(self, user):
        pass

    def collect(self):
        tmp = self._storage
        self._storage = []
        return tmp

    def observe(self):
        return tuple(self._storage)

    def put_in(self, *args):
        self._storage.extend(args)

    def move(self, user):
        ToDo

    def set_neighbour(self, **kwargs):
        self.left = kwargs.get("left", None)
        self.right = kwargs.get("right", None)
        self.up = kwargs.get("up", None)
        self.down = kwargs.get("down", None)

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
        if items is None:
            items = []
        self.stun_duration = stun_duration
        self.type = "Stun"

    def activate(self, user):
        ToDo


class RubberRoom(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        if items is None:
            items = []
        self.exit_destination = exit_destination
        self.type = "RubberRoom"

    def move(self, user):
        ToDo


class Teleport(Cell):
    def __init__(self, shift_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        if items is None:
            items = []
        self.shift_destination = shift_destination
        self.type = "Teleport"

    def show_accessible(self):
        ans = super().show_accessible()
        ans.append(self.shift_destination)
        return ans

    def set_shift_destination(self, shift_destination):
        self.shift_destination = shift_destination

    def activate(self, user):
        ToDo


class Armory(Cell):
    def __init__(self, ammunition=3, items=None, **kwargs):
        super().__init__(items, **kwargs)
        if items is None:
            items = []
        self.type = "Armory"
        self.ammunition = ammunition

    def activate(self, user):
        ToDo


class Exit(Cell):
    def __init__(self, exit_destination, items=None, **kwargs):
        super().__init__(items, **kwargs)
        if items is None:
            items = []
        self.exit_destination = exit_destination
        self.type = "Exit"

    def move(self, user):
        ToDo
