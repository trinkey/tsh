from .ansi import ansi
from .util import get_escape_string

from typing import Callable

def Delete(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    current_command = current_command[:cursor_position - 3:] + current_command[cursor_position + 1::]
    return (
        current_command,
        past_index,
        cursor_position - 3
    )

def Left(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    _ = current_command[max(0, cursor_position - 3):-2:]
    return (
        current_command[:cursor_position - 2:] + current_command[cursor_position::],
        past_index,
        max(0, cursor_position - 3)
    )

def Home(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command,
        past_index,
        0
    )

def End(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command,
        past_index,
        len(current_command)
    )

escape_sequences: dict[str, Callable] = {
    # 27 ... - unix
    get_escape_string([27, 91, 51, 126]): Delete,
    get_escape_string([27, 91, 68]): Left,
    get_escape_string([27, 91, 72]): Home,
    get_escape_string([27, 91, 70]): End,

    # 224 ... - nt
    get_escape_string([224, 83]): Delete,
    get_escape_string([224, 75]): Left,
    get_escape_string([224, 71]): Home,
    get_escape_string([224, 79]): End,

    # 0 ... - nt
    get_escape_string([0, 75]): Left,
    get_escape_string([0, 71]): Home,
    get_escape_string([0, 79]): End
}
