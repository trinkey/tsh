import socket
import os
import re

from readchar import readchar
from typing import Union

hostname: str = socket.gethostname()
username: str = os.getlogin()

def get_char() -> int:
    return ord(readchar())

def get_escape_string(sequence: list[int]) -> str:
    return "-".join([str(i) for i in sequence])

def ansi_length(text: Union[str, bytes]) -> int:
    if isinstance(text, str):
        return len(re.sub(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", "", text))
    return len(text)

def get_command_args(command: str) -> dict[str, list[str]]:
    quotes = False
    quote_type = ""
    escape = False
    param = False
    double_param = False
    string = ""
    output = {"args": [], "strings": []}

    for i in " ".join(command.split(" ")[1::]):
        if not (quotes or escape or string) and i == "-":
            if param and not double_param:
                double_param = True
            elif not param:
                param = True
            else:
                string += i

        elif i == " ":
            if escape or quotes:
                string += i

            elif param:
                if string:
                    output["args"].append(string)
                    string = ""

                param = False
                double_param = False

            else:
                if string:
                    output["strings"].append(string)
                    string = ""

        elif param:
            if double_param:
                string += i
            else:
                output["args"].append(i)

        elif not escape and not param and (i == "'" or i == "\"") and i != quote_type:
            quotes = True
            quote_type = i

        elif i == quote_type and not escape:
            quotes = False
            quote_type = ""

        # the inline if is only to fix windows fuckery where backslashes are used in paths
        elif i == ("`" if os.name == "nt" else "\\"):
            escape = not escape
            if not escape:
                string += i

        elif escape:
            if i == "n":
                string += "\n"
            elif i == "t":
                string += "\t"
            else:
                string += i

            escape = False

        else:
            string += i

    if string:
        output["args" if param else "strings"].append(string)

    return output

def bytes_to_human(count: Union[int, float]) -> str:
    sizes = "KMGTPEZY"
    index = 0
    size_str = ""

    while count > 1000:
        count = round(count / 100) / 10
        size_str = sizes[index]
        index += 1

    return str(count) + size_str

def pad_start(string: str, count: int, padding: str=" ") -> str:
    return padding * (count - ansi_length(string)) + string

def max_length(strings: list[str]) -> int:
    max_len = 0

    for i in strings:
        max_len = max(max_len, ansi_length(i))

    return max_len

def consistent_length(strings: list[str]) -> list[str]:
    new_strings = []
    max_len = max_length(strings)

    for i in strings:
        new_strings.append(pad_start(i, max_len))

    return new_strings
