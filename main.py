from lib import display as display
from lib import receiver as receiver
from lib import menu_facade as menu_facade


main_display = display.ConsoleDisplay()
main_receiver = receiver.SimpleConsoleReceiver()

main_body = menu_facade.MenuFacade(main_receiver, main_display)