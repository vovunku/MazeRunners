from lib import display as display
from lib import receiver as receiver
from lib import menu_facade as menu_facade
from lib import map_manager as map_manager


main_display = display.ConsoleDisplay()
main_receiver = receiver.SimpleConsoleReceiver()
main_map_manager = map_manager.ConsoleMapManager("/home/vovun/PycharmProjects/MazeRunners/maps")

main_body = menu_facade.MenuFacade(main_receiver, main_display, main_map_manager)
main_body.start_main_loop()