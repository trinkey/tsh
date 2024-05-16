from readchar import readchar
import socket
import os

from typing import Callable

hostname: str = socket.gethostname()
username: str = os.getlogin()

default_commands: list[tuple[str, str, Callable]] = [
    ("ls", "Lists the files in a directory.", lambda x: x)
]

def get_char() -> int:
    return ord(readchar())

def get_escape_string(sequence: list[int]) -> str:
    return "-".join([str(i) for i in sequence])
