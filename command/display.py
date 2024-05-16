import shutil
import sys
import os
import re

from pathlib import Path
from DotIndex import DotIndex

from .types import _CommandManager, _Display
from .ansi import ansi
from .util import username, hostname, get_escape_string
from .escape_sequences import escape_sequences

class Display(_Display):
    def __init__(self):
        self.current_input: str = ""
        self.escape_sequence: list[int] = []
        self.cursor_position: int = 0
        self.past_index: int = 0
        self.previous_line: str = ""

    def term_size(self) -> DotIndex:
        x = shutil.get_terminal_size()
        return DotIndex({"width": x.columns, "height": x.lines})

    def display_text(self, text: str, disable_auto_wrap: bool=False, allow_printing: bool=True) -> list[str]:
        if disable_auto_wrap:
            self._print(text)
            return [text]

        width = self.term_size().width # type: ignore
        chunks = []
        for block in text.split("\n"):
            chunk = ""
            first = True

            for word in block.split(" "):
                if self._string_length(f"{chunk} {word}") >= width:
                    chunks.append(chunk)
                    chunk = word
                else:
                    chunk += f"{'' if first else ' '}{word}"

                first = False

            chunks.append(chunk)

        if allow_printing:
            self._print("\n".join(chunks))

        return chunks

    def keyboard_event(self, key: int) -> None:
        # 27 91 51 126 delete
        # 27 91 65 up
        # 27 91 68 left
        # 27 91 66 down
        # 27 91 67 right
        # 27 91 53 126 pgup
        # 27 91 54 126 pgdn

        width = self.term_size().width # type: ignore

        if key == 3: # Ctrl + C
            self._print(f"{ansi.COLORS.TEXT.RED}^C{ansi.COLORS.RESET}\n{self._get_ps1()}") # type: ignore
            self.current_input = ""
            self.cursor_position = 0

        elif key == 4: # Ctrl + D
            self.display_text("exit\n")
            exit()

        elif key == 8: # Ctrl + Backspace (TODO)
            ...

        elif key == 9: # Tab (TODO)
            ...

        elif key == 10: # Enter
            temp = self.current_input
            self.current_input = ""
            self.cursor_position = 0

            self.display_text("\n")
            self.display_text(self.manager.command(temp) + self._get_ps1())

        elif key == 12: # Ctrl + L
            self.display_text(f"{ansi.ERASE.ALL}{ansi.CURSOR.HOME}")

        elif key == 13: # Carriage Return, ignored
            ...

        elif key == 27: # Escape, managed later
            ...

        elif key == 127: # Backspace
            if len(self.current_input):
                self.current_input = self.current_input[:max(0, self.cursor_position - 1):] + self.current_input[self.cursor_position::]
                self.cursor_position -= 1

        elif key >= 32 and key <= 126: # Text character
            self.display_text(chr(key))
            self._insert_character(chr(key))
            self.cursor_position += 1

        else: # Other control character
            self.display_text(str(key) + " ")

        if key == 27: # Escape character
            self.escape_sequence = [27]

        elif len(self.escape_sequence) and self.escape_sequence[0] == 27:
            self.escape_sequence.append(key)
            escape_string = get_escape_string(self.escape_sequence)

            if escape_string in escape_sequences:
                self.current_input, \
                self.past_index, \
                self.cursor_position, \
                temp = escape_sequences[escape_string].on_callback(
                    self.current_input,
                    self.manager.previous_commands,
                    self.past_index,
                    self.cursor_position
                )

                self._print(temp)

        ps1 = self._get_ps1()
        x = len(self.display_text(self.previous_line, allow_printing=False)) - 1
        curr = f"{ps1}{self.current_input}"
        self.previous_line = curr

        self.display_text(f"{ansi.CURSOR.LEFT(width)}{ansi.CURSOR.UP(x) if x else ''}{ansi.ERASE.SCREEN_PAST_CURSOR}")
        self.display_text(self._correct_cur_pos(
            self.display_text(curr),
            self._string_length(ps1)
        ))

    def _correct_cur_pos(self, string: list[str], ps1_length: int=0) -> str:
        remaining = self.cursor_position + ps1_length
        line_count = 0

        for i in string:
            remaining -= self._string_length(i)
            line_count += 1

            if remaining <= 0:
                if len(string) - line_count:
                    return f"{ansi.CURSOR.LEFT(len(string[-1]))}{ansi.CURSOR.UP(len(string) - line_count)}{ansi.CURSOR.RIGHT(self._string_length(i) - remaining)}"

                elif -remaining - 1 != 0:
                    return ansi.CURSOR.LEFT(-remaining - 1)

                else:
                    break

        return ""

    def _insert_character(self, char: str) -> None:
        self.current_input = self.current_input[:self.cursor_position:] + char + self.current_input[self.cursor_position::]

    def _start(self, default_path: Path=Path(os.path.expanduser("~/"))) -> None:
        self.path = default_path
        self.display_text(self._get_ps1())

    def _get_ps1(self) -> str:
        return f"{ansi.COLORS.TEXT.BRIGHT_GREEN}{ansi.STYLES.BOLD}{username}@{hostname}{ansi.COLORS.RESET}:{ansi.COLORS.TEXT.BRIGHT_BLUE}{ansi.STYLES.BOLD}{self.path}{ansi.COLORS.RESET}$ "

    def _string_length(self, text: str) -> int:
        return len(re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", text))

    def _print(self, text: str) -> None:
        print(text, end="")
        sys.stdout.flush()

    def _hook_manager(self, manager: _CommandManager) -> None:
        self.manager = manager
