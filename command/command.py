from typing import Callable
from .types import _CommandManager, _Command

class Command(_Command):
    def __init__(
        self,
        command_name: str,
        help_string: str,
        callback: Callable[..., str],
        container: _CommandManager
    ):
        self.command_name: str = command_name
        self.help_string: str = help_string
        self.callback: Callable = callback

        container.add_command(self)

    def __str__(self) -> str:
        return self.help_string
