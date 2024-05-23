from .ansi import ansi
from .types import _Command, _CommandManager
from .util import ansi_length, get_command_args

class CommandManager(_CommandManager):
    def __init__(self):
        self.commands: dict[str, _Command] = {}
        self.previous_commands = []

    def add_command(self, command: _Command):
        self.commands[command.command_name] = command

    def command(self, command: str) -> str:
        self.previous_commands.append(command)
        command_name = command.split(" ", 1)[0]
        width = self.display.term_size().width # type: ignore

        if command_name == "exit":
            exit()

        if not command_name:
            return ""

        if command_name == "help":
            output = f"{ansi.COLORS.TEXT.BRIGHT_BLACK}==={ansi.COLORS.RESET} tSH Help {ansi.COLORS.TEXT.BRIGHT_BLACK}==={ansi.COLORS.RESET}\n"
            output = ' ' * (min(50, width - ansi_length(output)) // 2) + output

            x = get_command_args(command)
            if len(x["strings"]):
                commands = x["strings"]
            else:
                commands = self.commands

            for command in commands:
                try:
                    output += f"{ansi.COLORS.TEXT.BRIGHT_YELLOW}{command}{ansi.COLORS.RESET}\n  {self.commands[command]}\n"
                except KeyError:
                    output += f"{ansi.COLORS.TEXT.RED}Unknown command '{command}'.\n"

            return output

        if command_name not in self.commands:
            return f"{ansi.COLORS.TEXT.RED}Unknown command '{command_name}'.{ansi.COLORS.RESET}\nYou can view a list of all commands with '{ansi.COLORS.TEXT.GREEN}help{ansi.COLORS.RESET}'.\n"

        try:
            return self.commands[command_name].callback(command, self.display.path)
        except PermissionError:
            return f"{ansi.COLORS.TEXT.RED}{command_name}: Permission denied.{ansi.COLORS.RESET}\n"
        except FileNotFoundError:
            return f"{ansi.COLORS.TEXT.RED}{command_name}: File not found.{ansi.COLORS.RESET}\n"

    def _hook_display(self, display) -> None:
        self.display = display
