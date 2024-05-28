import threading

from .command_manager import CommandManager
from .command import Command
from .display import Display
from .util import get_char
from .default_commands import default_commands

from typing import Callable, Union

display = Display()
command_manager = CommandManager()

def run(
    command_override: Union[list[tuple[str, str, Callable]], None] = None
):
    def th():
        for i in command_override or default_commands:
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
