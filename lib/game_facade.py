class GameFacade:
    """Accelerate game modules and allow interaction"""

    def __init__(self, receiver, board, players_list):
        self.receiver = receiver
        self.board = board
        self.players = players_list

    def make_turn(self, user_id, dest):
        self.players[user_id].move(dest)

    def game_loop(self):
        inp = self.receiver.handle_command()

