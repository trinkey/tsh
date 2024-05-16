from .ansi import ansi
from .util import get_escape_string

class EscapeSequence:
    sequence: list[int]

    @staticmethod
    def on_callback(
        current_command: str,
        past_commands: list[str],
        past_index: int,
        cursor_position: int
    ) -> tuple[str, int, int, str]: ...

class Delete(EscapeSequence):
    sequence = [27, 91, 51, 126]

    @staticmethod
    def on_callback(
        current_command: str,
        past_commands: list[str],
        past_index: int,
        cursor_position: int
    ) -> tuple[str, int, int, str]:
        current_command = current_command[:cursor_position - 3:] + current_command[cursor_position + 1::]
        return (
            current_command,
            past_index,
            cursor_position - 3,
            f"{ansi.CURSOR.LEFT(3)}{current_command[cursor_position + 1::]}    {ansi.CURSOR.LEFT(4 + len(current_command[cursor_position + 1::]))}"
        )

class Left(EscapeSequence):
    sequence = [27, 91, 68]

    @staticmethod
    def on_callback(
        current_command: str,
        past_commands: list[str],
        past_index: int,
        cursor_position: int
    ) -> tuple[str, int, int, str]:
        _ = current_command[max(0, cursor_position - 3):-2:]
        return (
            current_command[:-2:],
            past_index,
            max(0, cursor_position - 2),
            f"{ansi.CURSOR.LEFT(2)}{_}  {ansi.CURSOR.LEFT(min(len(current_command), len(_) + 3))}"
        )

escape_sequences: dict[str, type['EscapeSequence']] = {
    get_escape_string(Delete.sequence): Delete,
    get_escape_string(Left.sequence): Left
}
