from lib import display as display
from lib import receiver as receiver
from lib import menu_facade as menu_facade
import pathlib


main_display = display.ConsoleDisplay()
main_receiver = receiver.SimpleConsoleReceiver()
lib_path = str(pathlib.Path(__file__).parent.absolute()) + "/maps"
main_display.message("Path to maps: {0}".format(lib_path))

main_body = menu_facade.MenuFacade(main_receiver, main_display, lib_path)
main_body.start_main_loop()