import pathlib
import stat
import os

from .util import get_command_args, bytes_to_human, max_length, pad_start
from .ansi import ansi

from typing import Callable

def test_args(command: str, path: pathlib.Path) -> str:
    return str(get_command_args(command)) + "\n"

def ls(command: str, path: pathlib.Path) -> str:
    def sort(a):
        if "s" in args["args"]:
            ... # sort by filesize

        if "t" in args["args"]:
            ... # sort by time modified

        if a[0] == ".":
            a = a[1::]
        return a.lower()

    args = get_command_args(command)
    directories = os.listdir(path)

    if "l" in args["args"]:
        temp_strings = []

        if "L" in args["args"]:
            temp_strings.append([
                "perms",
                "owner",
                "group",
                "size",
                "name",
                ""
            ])

        strings = []
        joiner = "\n"
        include_space_on_filenames = False

        for i in directories:
            abs_file = path / i
            link = os.path.islink(abs_file)
            file = pathlib.Path(os.readlink(abs_file)) if link else abs_file

            if not include_space_on_filenames and (" " in str(file.stem) + str(abs_file.stem)):
                include_space_on_filenames = True

            try:
                temp_strings.append([
                    stat.filemode(os.stat(abs_file, follow_symlinks=False).st_mode),
                    file.owner(),
                    file.group(),
                    (bytes_to_human if "h" in args["args"] else str)(os.path.getsize(file)),
                    f"{abs_file.stem} -> {file}" if link else str(file.stem)
                ])

                if link:
                    color = ansi.COLORS.TEXT.BRIGHT_YELLOW
                elif os.path.isdir(abs_file):
                    color = ansi.COLORS.TEXT.BRIGHT_BLUE
                elif temp_strings[-1][0][6] == "x":
                    color = ansi.COLORS.TEXT.BRIGHT_GREEN
                else:
                    color = ""

                temp_strings[-1].append(color)

            except FileNotFoundError:
                temp_strings.append([
                    stat.filemode(os.stat(abs_file, follow_symlinks=False).st_mode),
                    "-",
                    "-",
                    "0",
                    f"{abs_file.stem} -> {file}" if link else str(file.stem),
                    ansi.COLORS.TEXT.BRIGHT_RED
                ])

        inverse_temp_strings = [
            [], [], []
        ]

        for i in temp_strings:
            inverse_temp_strings[0].append(i[1])
            inverse_temp_strings[1].append(i[2])
            inverse_temp_strings[2].append(i[3])

        maxes = [
            max_length(inverse_temp_strings[0]),
            max_length(inverse_temp_strings[1]),
            max_length(inverse_temp_strings[2])
        ]

        SQUO = "'"
        strings = [str(path), ""] + [f"{i[0]} {pad_start(i[1], maxes[0])} {pad_start(i[2], maxes[1])} {pad_start(i[3], maxes[2])} {i[5]}{SQUO if ' ' in i[4] else ' ' if include_space_on_filenames else ''}{i[4]}{SQUO if ' ' in i[4] else ''}{ansi.COLORS.RESET}" for i in temp_strings]

    else:
        strings = sorted(directories, key=sort, reverse="r" in args["args"])
        joiner = " "

    return joiner.join(strings) + "\n"

def not_implemented(command, path) -> str:
    return f"{ansi.COLORS.TEXT.RED}Not implemented :3{ansi.COLORS.RESET}\n"

default_commands: list[tuple[str, str, Callable]] = [
    ("test", "Returns all of the arguments passed into the command. Used for debugging.", test_args),
    ("ls", "Lists the files in the current directory.", ls),
    ("cd", "Not implemented :3", not_implemented),
    ("cat", "Not implemented :3", not_implemented),
    ("echo", "Not implemented :3", not_implemented),
    ("touch", "Not implemented :3", not_implemented),
    ("mkdir", "Not implemented :3", not_implemented),
    ("mv", "Not implemented :3", not_implemented),
    ("cp", "Not implemented :3", not_implemented)
]
