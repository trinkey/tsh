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
            try:
                return os.path.getsize(path / a)
            except FileNotFoundError:
                print("a")
                return 0

        if "t" in args["args"]:
            return os.path.getmtime(path / a)

        if a[0] == ".":
            a = a[1::]
        return a.lower()

    args = get_command_args(command)

    for i in args["args"]:
        if i not in "aAhlLrst":
            return f"{ansi.COLORS.TEXT.RED}Invalid argument '{i}'.{ansi.COLORS.RESET}\nYou can view the command format by running '{ansi.COLORS.TEXT.GREEN}help ls{ansi.COLORS.RESET}'.\n"

    if len(args["strings"]) == 1:
        if args["strings"][0][0] == "/":
            path = pathlib.Path(args["strings"][0])
        elif args["strings"][0][0] == "~":
            path = pathlib.Path(os.path.expanduser(args["strings"][0]))
        else:
            path = path / args["strings"][0]

    elif len(args["strings"]) > 1:
        return f"{ansi.COLORS.TEXT.RED}ls: Invalid amount of arg strings (expected 0-1, got {len(args['strings'])}){ansi.COLORS.RESET}\n"

    directories = os.listdir(path)

    if "a" in args["args"]:
        directories = [".", ".."] + directories
    elif "A" not in args["args"]:
        directories = [i for i in directories if i[0] != "."]

    directories = sorted(directories, key=sort, reverse="r" in args["args"])
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
    include_full_link = "l" in args["args"]

    for i in directories:
        abs_file = path / i
        link = os.path.islink(abs_file)

        if link:
            x = os.readlink(abs_file)
            file = pathlib.Path(("/" if x[0] not in "~/" else "") + (os.path.expanduser(x) if x[0] == "~" else x))
        else:
            file = abs_file

        if not include_space_on_filenames and (" " in str(file.name) + str(abs_file.name)):
            include_space_on_filenames = True

        try:
            if os.name == "nt":
                temp_strings.append([
                    stat.filemode(os.stat(abs_file, follow_symlinks=False).st_mode),
                    "",
                    "",
                    (bytes_to_human if "h" in args["args"] else str)(os.path.getsize(file)),
                    f"{abs_file.name} -> {file}" if include_full_link and link else str(file.name) if i != "." else "."
                ])
            else:
                temp_strings.append([
                    stat.filemode(os.stat(abs_file, follow_symlinks=False).st_mode),
                    file.owner(),
                    file.group(),
                    (bytes_to_human if "h" in args["args"] else str)(os.path.getsize(file)),
                    f"{abs_file.name} -> {file}" if include_full_link and link else str(file.name) if i != "." else "."
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
                f"{abs_file.name} -> {file}" if include_full_link and link else str(file.name),
                ansi.COLORS.TEXT.RED
            ])

    SQUO = "'"

    if "l" in args["args"]:
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

        strings = [str(path), ""] + [f"{pad_start(i[0], 10)}" + ("" if os.name == "nt" else f" {pad_start(i[1], maxes[0])} {pad_start(i[2], maxes[1])}") + f" {pad_start(i[3], maxes[2])} {i[5]}{'' if not include_space_on_filenames else SQUO if ' ' in i[4] else ' '}{i[4]}{SQUO if ' ' in i[4] and include_space_on_filenames else ''}{ansi.COLORS.RESET}" for i in temp_strings]
        joiner = "\n"

    else:
        strings = [f"{i[5]}{'' if not include_space_on_filenames else SQUO if ' ' in i[4] else ' '}{i[4]}{SQUO if ' ' in i[4] and include_space_on_filenames else ''}{ansi.COLORS.RESET}" for i in temp_strings]
        joiner = "  "

    return joiner.join(strings) + "\n"

def clear(command: str, path: pathlib.Path) -> str:
    return f"{ansi.ERASE.SAVED_LINES}{ansi.CURSOR.HOME}"

def cat(command: str, path: pathlib.Path) -> str:
    args = get_command_args(command)

    for i in args["args"]:
        if i not in "cnNs":
            return f"{ansi.COLORS.TEXT.RED}Invalid argument '{i}'.{ansi.COLORS.RESET}\nYou can view the command format by running '{ansi.COLORS.TEXT.GREEN}help cat{ansi.COLORS.RESET}'.\n"

    if not len(args["strings"]):
        return f"{ansi.COLORS.TEXT.RED}cat: File not specified.{ansi.COLORS.RESET}\n"

    file = pathlib.Path
    output = ""

    for i in args["strings"]:
        try:
            abs_file = path / i if i[0] not in "~/" else pathlib.Path(os.path.expanduser(i))
            link = os.path.islink(abs_file)

            if link:
                x = os.readlink(abs_file)
                file = pathlib.Path(("/" if x[0] not in "~/" else "") + (os.path.expanduser(x) if x[0] == "~" else x))
            else:
                file = abs_file

            f = open(file, "rb").read().decode('utf-8', errors='replace')

            if "c" in args["args"]:
                output += f"{len(f)}\n"

            elif "n" in args["args"] or "N" in args["args"] or "s" in args["args"]:
                ...

            else:
                output += f"{f}\n"

        except IsADirectoryError:
            output += f"{ansi.COLORS.TEXT.RED}cat: {file} is a directory{ansi.COLORS.RESET}\n"
        except FileNotFoundError:
            output += f"{ansi.COLORS.TEXT.RED}cat: {file} not found{ansi.COLORS.RESET}\n"
        except PermissionError:
            output += f"{ansi.COLORS.TEXT.RED}cat: Permission denied{ansi.COLORS.RESET}\n"

    return output

def not_implemented(command: str, path: pathlib.Path) -> str:
    return f"{ansi.COLORS.TEXT.RED}Not implemented :3{ansi.COLORS.RESET}\n"

default_commands: list[tuple[str, str, Callable]] = [
    ("test", "Returns all of the arguments passed into the command. Used for debugging.", test_args),
    ("ls", "Lists the files in the current directory. Usage: ls [-aAhlLrst] [path]\n    -a - List all files\n    -A - List all except root and parent\n    -h - Human readable file sizes\n    -l - Long format\n    -L - Label columns (only works with -l)\n    -r - Reverse order\n    -s - Sort by file size\n    -t - Sort by date modified", ls),
    ("cd", "Not implemented :3", not_implemented),
    ("cat", "Displays the contents of a file. Usage: cat [-cnNs --crlf] [path[, path2, ...]]\n    -c - Returns only the character count\n    -n - Numbers the lines\n    -N - Numbers non-empty lines\n    -s - Don't display blank lines\n    --crlf - Use a carriage return followed by a line feed as the line ending. This overrides the default of just a single line feed", cat),
    ("echo", "Not implemented :3", not_implemented),
    ("touch", "Not implemented :3", not_implemented),
    ("mkdir", "Not implemented :3", not_implemented),
    ("mv", "Not implemented :3", not_implemented),
    ("cp", "Not implemented :3", not_implemented),
    ("clear", "Clears the screen and ALL of the display history. Command history (accessed via up/down buttons) is still saved.", clear)
]
