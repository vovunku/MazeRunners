class Player:
    """Simplest player"""

    def __int__(self, field, x, y):
        self.type = "Abstract"
        self.backpack = {"Ammo": 0}
        self.statement = {"Stun": 0}
        self.coords = {"Field": field, "X": x, "Y": y}

    def check_backpack(self):
        return self.backpack

    def check_statement(self):
        return self.statement
