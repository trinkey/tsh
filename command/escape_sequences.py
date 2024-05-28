import os

from .util import get_escape_string, ansi_length

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

def up(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    if past_index + 1 > len(past_commands):
        return (
            current_command[:-1 if os.name == "nt" else -2:],
            past_index,
            cursor_position
        )

    return (
        past_commands[-past_index - 1],
        past_index + 1,
        ansi_length(past_commands[-past_index - 1])
    )

def down(
    current_command: str,
    past_commands: list[str],
    past_index: int,
    cursor_position: int
) -> tuple[str, int, int]:
    if past_index <= 1:
        return (
            "",
            0,
            0
        )

    return (
        past_commands[-past_index + 1],
        past_index - 1,
        ansi_length(past_commands[-past_index + 1])
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
        min(ansi_length(current_command), cursor_position - (0 if os.name == "nt" else 1))
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
        ansi_length(current_command) - (1 if os.name == "nt" else 2)
    )

escape_sequences: dict[str, Callable] = {
    # 27 ... - unix
    get_escape_string([27, 91, 51, 126]): delete,
    get_escape_string([27, 91, 65]): up,
    get_escape_string([27, 91, 66]): down,
    get_escape_string([27, 91, 68]): left,
    get_escape_string([27, 91, 67]): right,
    get_escape_string([27, 91, 72]): home,
    get_escape_string([27, 91, 70]): end,

    # 224 ... - nt
    get_escape_string([224, 83]): delete,
    get_escape_string([224, 72]): up,
    get_escape_string([224, 80]): down,
    get_escape_string([224, 75]): left,
    get_escape_string([224, 77]): right,
    get_escape_string([224, 71]): home,
    get_escape_string([224, 79]): end,

    # 0 ... - nt
    get_escape_string([0, 72]): up,
    get_escape_string([0, 80]): down,
    get_escape_string([0, 75]): left,
    get_escape_string([0, 77]): right,
    get_escape_string([0, 71]): home,
    get_escape_string([0, 79]): end
}
