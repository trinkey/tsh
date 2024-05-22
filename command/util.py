import socket
import os
import re

from .ansi import ansi

from readchar import readchar
from typing import Callable

hostname: str = socket.gethostname()
username: str = os.getlogin()

default_commands: list[tuple[str, str, Callable]] = [
    ("ls", "Lists the files in a directory.", lambda command, path: f"{' '.join(os.listdir(path))}\n")
]

def get_char() -> int:
    return ord(readchar())

def get_escape_string(sequence: list[int]) -> str:
    return "-".join([str(i) for i in sequence])

def ansi_length(text: str) -> int:
    return len(re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", text))
