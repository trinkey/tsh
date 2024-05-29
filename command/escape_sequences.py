import random
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
    x = current_command[:cursor_position - (1 if os.name == "nt" else 2):] + current_command[cursor_position::]

    return (
        x,
        past_index,
        min(ansi_length(x), cursor_position - (0 if os.name == "nt" else 1))
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

def get_empty(length) -> Callable:
    def x(
        current_command: str,
        past_commands: list[str],
        past_index: int,
        cursor_position: int
    ) -> tuple[str, int, int]:
        return (
            current_command[:cursor_position - length:] + current_command[cursor_position::],
            past_index,
            cursor_position
        )

    x.__name__ = str(random.random())
    return x

escape_sequences: dict[str, Callable] = {
    # 27 ... - unix
    get_escape_string([27, 91, 51, 126]): delete,
    get_escape_string([27, 91, 65]): up,
    get_escape_string([27, 91, 66]): down,
    get_escape_string([27, 91, 68]): left,
    get_escape_string([27, 91, 67]): right,
    get_escape_string([27, 91, 72]): home,
    get_escape_string([27, 91, 70]): end,
    get_escape_string([27, 91, 53, 126]): get_empty(3), # pg up
    get_escape_string([27, 91, 54, 126]): get_empty(3), # pg dn

    # 224 ... - nt
    get_escape_string([224, 83]): delete,
    get_escape_string([224, 72]): up,
    get_escape_string([224, 80]): down,
    get_escape_string([224, 75]): left,
    get_escape_string([224, 77]): right,
    get_escape_string([224, 71]): home,
    get_escape_string([224, 79]): end,
    get_escape_string([224, 73]): get_empty(1), # pg up
    get_escape_string([224, 81]): get_empty(1), # pg dn

    # 0 ... - nt
    get_escape_string([0, 72]): up,
    get_escape_string([0, 80]): down,
    get_escape_string([0, 75]): left,
    get_escape_string([0, 77]): right,
    get_escape_string([0, 71]): home,
    get_escape_string([0, 79]): end,
    get_escape_string([0, 73]): get_empty(1), # pg up
    get_escape_string([0, 81]): get_empty(1) # pg dn
}
