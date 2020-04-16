import handler
import receiver
import display


class GameFacade:
    """Accelerate game modules and allow interaction"""

    def __init__(self, receiver, display, board, players_dict):
        self.receiver = receiver
        self.display = display
        self.board = board
        self.players = players_dict

    def game_loop(self):
        activate_phase = handler.ActivateHandler(self, self.display, self.receiver, "Activating phase has begun")
        act_phase = handler.ActHandler(self, self.display, self.receiver, "Moving phase has begun")
        end_phase = handler.AskingHandler(self, self.display, self.receiver, "End phase has begun")
        activate_phase.set_next(act_phase)
        act_phase.set_next(end_phase)
        for player_id in self.players:
            self.display.message("{0} turn has begun".format(player_id))
            activate_phase.handle(player_id)


rec = receiver.SimpleConsoleReceiver()
dep = display.ConsoleDisplay()


GameFacade(rec, dep, )