from .command_manager import CommandManager
from .command import Command
from .display import Display
from .util import default_commands, get_char
from .types import _Display as display

from typing import Callable

display = Display()
command_manager = CommandManager()

def run(
    command_override: list[tuple[str, str, Callable]] | None = None
):
    import threading

    def th():
        global display, command_manager
        if command_override is None:
            for i in default_commands:
                Command(
                    i[0], i[1], i[2],
                    command_manager
                )

        else:
            for i in command_override:
                Command(
                    i[0], i[1], i[2],
                    command_manager
                )

        display._hook_manager(command_manager)
        command_manager._hook_display(display)

        display._start()

    thread = threading.Thread(target=th)
    thread.start()

    while True:
        try:
            display.keyboard_event(get_char())
        except KeyboardInterrupt:
            display.keyboard_event(-1)
        except EOFError:
            display.keyboard_event(-2)
