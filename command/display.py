import shutil
import sys
import os

from pathlib import Path
from DotIndex import DotIndex

from .types import _CommandManager, _Display
from .ansi import ansi
from .util import username, hostname, get_escape_string, ansi_length
from .escape_sequences import escape_sequences

class Display(_Display):
    def __init__(self):
        self.current_input: str = ""
        self.escape_sequence: list[int] = []
        self.cursor_position: int = 0
        self.past_index: int = 0
        self.previous_line: str = ""
        self.prev_lines_up: int = 0

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
                if ansi_length(f"{chunk} {word}") >= width:
                    chunks.append(chunk)
                    while ansi_length(word) >= width:
                        chunks.append(word[:width:])
                        word = word[width::]

                    chunk = word
                else:
                    chunk += f"{'' if first else ' '}{word}"

                first = False

            chunks.append(chunk)

        if allow_printing:
            self._print("\n".join(chunks))

        return chunks

    def keyboard_event(self, key: int) -> None:
        width = self.term_size().width # type: ignore

        if key == 3: # Ctrl + C
            self._print(f"{ansi.COLORS.TEXT.RED}^C{ansi.COLORS.RESET}\n{self._get_ps1()}") # type: ignore
            self.current_input = ""
            self.cursor_position = 0
            self.prev_lines_up = 0
            self.previous_line = ""

        elif key == 4: # Ctrl + D
            self.display_text("exit\n")
            exit()

        elif key == 9: # Tab (TODO)
            ...

        elif key == 10 or key == 13: # Enter (10: unix / 13: nt)
            temp = self.current_input
            self.current_input = ""
            self.cursor_position = 0
            self.previous_line = ""

            self.display_text("\n" + (ansi.CURSOR.DOWN(self.prev_lines_up) if self.prev_lines_up else ''))
            self.display_text(self.manager.command(temp) + self._get_ps1())

            self.prev_lines_up = 0

        elif key == 12: # Ctrl + L
            self.display_text(f"{ansi.ERASE.ALL}{ansi.CURSOR.HOME}")

        elif key == 0 or key == 27 or key == 224: # Escape (27: unix, 0/224: nt), managed later
            ...

        elif key == 8 or key == 127: # Backspace (8: nt / 127: unix)
            if len(self.current_input) and self.cursor_position > 0:
                self.current_input = self.current_input[:max(0, self.cursor_position - 1):] + self.current_input[self.cursor_position::]
                self.cursor_position -= 1

        elif key >= 32 and key <= 126: # Text character
            self.display_text(chr(key))
            self._insert_character(chr(key))
            self.cursor_position += 1

        else: # Other control character
            ... # Debugging: self.display_text(str(key) + " ")

        if key == 0 or key == 27 or key == 224: # Escape character
            self.escape_sequence = [key]

        elif len(self.escape_sequence) > 0 and len(self.escape_sequence) <= 5 and self.escape_sequence[0] == 27:
            self.escape_sequence.append(key)
            escape_string = get_escape_string(self.escape_sequence)

            if escape_string in escape_sequences:
                self.current_input, \
                self.past_index, \
                self.cursor_position = escape_sequences[escape_string](
                    self.current_input,
                    self.manager.previous_commands,
                    self.past_index,
                    self.cursor_position
                )

        ps1 = self._get_ps1()
        x = len(self.display_text(self.previous_line, allow_printing=False)) - 1 - self.prev_lines_up
        curr = f"{ps1}{self.current_input}"
        self.previous_line = curr

        self.display_text(f"{ansi.CURSOR.LEFT(width)}{ansi.CURSOR.UP(x) if x else ''}{ansi.ERASE.SCREEN_PAST_CURSOR}")
        self.display_text(self._correct_cur_pos(
            self.display_text(curr),
            ansi_length(ps1)
        ))

        sys.stdout.flush()

    def _correct_cur_pos(self, string: list[str], ps1_length: int=0) -> str:
        remaining = self.cursor_position + ps1_length - 1
        self.prev_lines_up = 0
        line_count = 0

        for i in string:
            remaining -= ansi_length(i)
            line_count += 1

            if remaining < 0:
                if len(string) - line_count:
                    self.prev_lines_up = len(string) - line_count

                    left = ansi_length(string[-1])
                    up = self.prev_lines_up
                    right = ansi_length(i) + remaining + (0 if line_count else 1)

                    return f"{ansi.CURSOR.LEFT(left)}{ansi.CURSOR.UP(up)}{ansi.CURSOR.RIGHT(right) if right > 0 else ''}"

                elif -remaining - 1 if len(string) == 1 else -remaining:
                    return ansi.CURSOR.LEFT(-remaining - 1 if len(string) == 1 else -remaining)

                else:
                    break

        return ""

    def _insert_character(self, char: str) -> None:
        self.current_input = self.current_input[:self.cursor_position:] + char + self.current_input[self.cursor_position::]

    def _start(self, default_path: Path=Path(os.path.expanduser("~/"))) -> None:
        self.path = default_path
        self.display_text(self._get_ps1())
        sys.stdout.flush()

    def _get_ps1(self) -> str:
        return f"{ansi.COLORS.TEXT.BRIGHT_GREEN}{ansi.STYLES.BOLD}{username}@{hostname}{ansi.COLORS.RESET}:{ansi.COLORS.TEXT.BRIGHT_BLUE}{ansi.STYLES.BOLD}{self.path}{ansi.COLORS.RESET}$ "

    def _print(self, text: str) -> None:
        print(text, end="")

    def _hook_manager(self, manager: _CommandManager) -> None:
        self.manager = manager
