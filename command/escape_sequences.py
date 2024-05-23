import os

from .util import get_escape_string

from typing import Callable

def delete(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    current_command = current_command[:cursor_position - (1 if os.name == "nt" else 3):] + current_command[cursor_position + 1::]
    return (
        current_command,
        past_index,
        cursor_position - (1 if os.name == "nt" else 3)
    )

def left(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command[:cursor_position - (1 if os.name == "nt" else 2):] + current_command[cursor_position::],
        past_index,
        max(0, cursor_position - (2 if os.name == "nt" else 3))
    )

def right(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command[:cursor_position - (1 if os.name == "nt" else 2):] + current_command[cursor_position::],
        past_index,
        min(len(current_command), cursor_position - (0 if os.name == "nt" else 1))
    )

def home(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command[:cursor_position - (1 if os.name == "nt" else 2):] + current_command[cursor_position::],
        past_index,
        0
    )

def end(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    return (
        current_command[:cursor_position - (1 if os.name == "nt" else 2):] + current_command[cursor_position::],
        past_index,
        len(current_command) - (1 if os.name == "nt" else 2)
    )

escape_sequences: dict[str, Callable] = {
    # 27 ... - unix
    get_escape_string([27, 91, 51, 126]): delete,
    get_escape_string([27, 91, 68]): left,
    get_escape_string([27, 91, 67]): right,
    get_escape_string([27, 91, 72]): home,
    get_escape_string([27, 91, 70]): end,

    # 224 ... - nt
    get_escape_string([224, 83]): delete,
    get_escape_string([224, 75]): left,
    get_escape_string([224, 77]): right,
    get_escape_string([224, 71]): home,
    get_escape_string([224, 79]): end,

    # 0 ... - nt
    get_escape_string([0, 75]): left,
    get_escape_string([0, 71]): home,
    get_escape_string([0, 79]): end
}
