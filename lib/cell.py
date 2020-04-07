class Cell:
    def __init__(self):
        self._left_is_free = False
        self._right_is_free = False
        self._up_is_free = False
        self._down_is_free = False
        self._storage = []
        self._type = "Empty"

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


class StunCell(Cell):
    def __init__(self, stun_duration):
        super().__init__()
        self._stun_duration = stun_duration
        self._type = "Stun"

    def activate(self, user):
        ToDo


class RubberCell(Cell):
    def __init__(self, exit_destination):
        super().__init__()
        self._exit_destination = exit_destination
        self._type = "RubberRoom"

    def move(self, user):
        ToDo


class TeleportCell(Cell):
    def __init__(self, shift_destination):
        super().__init__()
        self._shift_destination = shift_destination
        self._type = "Teleport"

    def activate(self, user):
        ToDo


class ArmoryCell(Cell):
    def __init__(self):
        super().__init__()
        self._type = "Armory"

    def activate(self, user):
        ToDo


class ExitCell(Cell):
    def __init__(self, exit_destination):
        super().__init__()
        self._exit_destination = exit_destination
        self._type = "Exit"

    def move(self, user):
        ToDo
