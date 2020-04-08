from lib import display as display
from lib import receiver as receiver


main_display = display.ConsoleDisplay()
main_receiver = receiver.SimpleConsoleReceiver()

running = True

while running:
    main_display.menu()
    inp = main_receiver.handle_string()
    main_display.message(str(inp))
