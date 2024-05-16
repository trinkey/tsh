from .ansi import ansi
from .types import _Command, _CommandManager

class CommandManager(_CommandManager):
    def __init__(self):
        self.commands: dict[str, _Command] = {}
        self.previous_commands = []

    def add_command(self, command: _Command):
        self.commands[command.command_name] = command

    def command(self, command: str) -> str:
        self.previous_commands.append(command)
        command_name = command.split(" ", 1)[0]

        if command_name == "exit":
            exit()

        if not command_name:
            return ""

        width = self.display.term_size().width # type: ignore
        if command_name == "help":
            output = f"{ansi.COLORS.TEXT.BRIGHT_BLACK}==={ansi.COLORS.RESET} Help {ansi.COLORS.TEXT.BRIGHT_BLACK}==={ansi.COLORS.RESET}\n"
            output = ' ' * (min(20, width - self.display._string_length(output)) // 2) + output

            for command in self.commands:
                output += f"{ansi.COLORS.TEXT.BRIGHT_YELLOW}{command}{ansi.COLORS.RESET}\n  {self.commands[command]}"

            return output + "\n"

        if command_name not in self.commands:
            return f"{ansi.COLORS.TEXT.RED}Unknown command '{command_name}'.{ansi.COLORS.RESET}\nYou can view a list of all commands with '{ansi.COLORS.TEXT.GREEN}help{ansi.COLORS.RESET}'.\n"

        return ""

    def _hook_display(self, display) -> None:
        self.display = display
