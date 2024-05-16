class ansi:
    __all__ = [
        "__all__",

        "ANSI_ESCAPE",

        "COLORS", "COLOR", "COLOURS", "COLOUR",
        "STYLES", "STYLE",
        "CURSOR",
        "ERASE"
    ]

    ANSI_ESCAPE  = "\x1b"

    class COLORS:
        __all__ = [
            "__all__",

            "RESET_ALL", "RESET",

            "TEXT",
            "BACKGROUND", "BG"
        ]

        RESET_ALL : str = "\x1b[0m" # Also resets styles
        RESET     : str = RESET_ALL

        class TEXT:
            __all__ = [
                "__all__",

                "RESET_ALL", "RESET",

                "DEFAULT",
                "BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE",
                "BRIGHT_BLACK", "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE",

                "EXTENDED_256",
                "RGB", "rgb"
            ]

            RESET_ALL      : str = "\x1b[0m" # Also resets styles and background color
            RESET          : str = RESET_ALL
            BLACK          : str = "\x1b[30m"
            RED            : str = "\x1b[31m"
            GREEN          : str = "\x1b[32m"
            YELLOW         : str = "\x1b[33m"
            BLUE           : str = "\x1b[34m"
            MAGENTA        : str = "\x1b[35m"
            CYAN           : str = "\x1b[36m"
            WHITE          : str = "\x1b[37m"
            DEFAULT        : str = "\x1b[39m"
            BRIGHT_BLACK   : str = "\x1b[90m"
            BRIGHT_RED     : str = "\x1b[91m"
            BRIGHT_GREEN   : str = "\x1b[92m"
            BRIGHT_YELLOW  : str = "\x1b[93m"
            BRIGHT_BLUE    : str = "\x1b[94m"
            BRIGHT_MAGENTA : str = "\x1b[95m"
            BRIGHT_CYAN    : str = "\x1b[96m"
            BRIGHT_WHITE   : str = "\x1b[97m"

            @staticmethod
            def EXTENDED_256 (num: int)                        -> str: return f"\x1b[38;5;{num}"
            @staticmethod
            def RGB          (red: int, green: int, blue: int) -> str: return f"\x1b[38;2;{red};{green};{blue}m"

            rgb = RGB

        class BACKGROUND:
            __all__ = [
                "__all__",

                "RESET_ALL", "RESET",

                "DEFAULT",
                "BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE",
                "BRIGHT_BLACK", "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE",

                "EXTENDED_256",
                "RGB", "rgb"
            ]

            RESET_ALL      : str = "\x1b[0m" # Also resets styles and text color
            RESET          : str = RESET_ALL
            BLACK          : str = "\x1b[40m"
            RED            : str = "\x1b[41m"
            GREEN          : str = "\x1b[42m"
            YELLOW         : str = "\x1b[43m"
            BLUE           : str = "\x1b[44m"
            MAGENTA        : str = "\x1b[45m"
            CYAN           : str = "\x1b[46m"
            WHITE          : str = "\x1b[47m"
            DEFAULT        : str = "\x1b[49m"
            BRIGHT_BLACK   : str = "\x1b[100m"
            BRIGHT_RED     : str = "\x1b[101m"
            BRIGHT_GREEN   : str = "\x1b[102m"
            BRIGHT_YELLOW  : str = "\x1b[103m"
            BRIGHT_BLUE    : str = "\x1b[104m"
            BRIGHT_MAGENTA : str = "\x1b[105m"
            BRIGHT_CYAN    : str = "\x1b[106m"
            BRIGHT_WHITE   : str = "\x1b[107m"

            @staticmethod
            def EXTENDED_256 (num: int)                        -> str: return f"\x1b[48;5;{num}"
            @staticmethod
            def RGB          (red: int, green: int, blue: int) -> str: return f"\x1b[48;2;{red};{green};{blue}m"

            rgb = RGB

        BG: type[BACKGROUND] = BACKGROUND

    class STYLES:
        __all__ = [
            "__all__",

            "RESET_ALL", "RESET",

            "BOLD", "DIM", "ITALIC", "UNDERLINE", "BLINK", "REVERSE", "INVISIBLE", "STRIKETHROUGH", "DOUBLE_UNDERLINE",
            "RESET_BOLD", "RESET_DIM", "RESET_ITALIC", "RESET_UNDERLINE", "RESET_BLINK", "RESET_REVERSE", "RESET_INVISIBLE", "RESET_STRIKETHROUGH"
        ]

        RESET_ALL           : str = "\x1b[0m" # Also resets color
        RESET               : str = RESET_ALL
        BOLD                : str = "\x1b[1m"
        DIM                 : str = "\x1b[2m"
        ITALIC              : str = "\x1b[3m"
        UNDERLINE           : str = "\x1b[4m"
        BLINK               : str = "\x1b[5m"
        REVERSE             : str = "\x1b[7m"
        INVISIBLE           : str = "\x1b[8m"
        STRIKETHROUGH       : str = "\x1b[9m"
        DOUBLE_UNDERLINE    : str = "\x1b[21m"
        RESET_BOLD          : str = "\x1b[22m"
        RESET_DIM           : str = "\x1b[22m"
        RESET_ITALIC        : str = "\x1b[23m"
        RESET_UNDERLINE     : str = "\x1b[24m"
        RESET_BLINK         : str = "\x1b[25m"
        RESET_REVERSE       : str = "\x1b[27m"
        RESET_INVISIBLE     : str = "\x1b[28m"
        RESET_STRIKETHROUGH : str = "\x1b[29m"

    class CURSOR:
        __all__ = [
            "__all__",

            "HOME",
            "UP_ONE",
            "SAVE_POSITION", "RESTORE_POSITION", "REQUEST_POSITION"
            "HIDE", "SHOW"

            "MOVE_TO", "MOVE_TO_ALT",
            "UP", "DOWN", "RIGHT", "LEFT"
            "NEXT_LINE", "PREVIOUS_LINE",
            "SET_COLUMN"
        ]

        HOME                 : str = "\x1b[H"
        UP_ONE               : str = "\x1bM"
        SAVE_POSITION        : str = "\x1b7"
        RESTORE_POSITION     : str = "\x1b8"
        HIDE                 : str = "\x1b[?25l"
        SHOW                 : str = "\x1b[?25h"

        # When printed, the position of the cursor is printed as
        # `\x1b[L;CR` where L is the line and C is the column.
        REQUEST_POSITION: str = "\x1b[6n"

        @staticmethod
        def MOVE_TO       (line: int, column: int) -> str: return f"\x1b[{line};{column}H"
        @staticmethod
        def MOVE_TO_ALT   (line: int, column: int) -> str: return f"\x1b[{line};{column}f"
        @staticmethod
        def UP            (lines: int)             -> str: return f"\x1b[{lines}A"
        @staticmethod
        def DOWN          (lines: int)             -> str: return f"\x1b[{lines}B"
        @staticmethod
        def RIGHT         (columns: int)           -> str: return f"\x1b[{columns}C"
        @staticmethod
        def LEFT          (columns: int)           -> str: return f"\x1b[{columns}D"
        @staticmethod
        def NEXT_LINE     (lines: int)             -> str: return f"\x1b[{lines}E"
        @staticmethod
        def PREVIOUS_LINE (lines: int)             -> str: return f"\x1b[{lines}F"
        @staticmethod
        def SET_COLUMN    (column: int)            -> str: return f"\x1b[{column}G"

    class ERASE:
        __all__ = [
            "__all__",

            "SCREEN_PAST_CURSOR", "SCREEN_PAST_CURSOR_ALT", "SCREEN_BEFORE_CURSOR",
            "ALL",
            "SAVED_LINES",
            "LINE_PAST_CURSOR", "LINE_PAST_CURSOR_ALT", "LINE_BEFORE_CURSOR",
            "LINE",
            "SAVE_SCREEN", "RESTORE_SCREEN"
        ]

        SCREEN_PAST_CURSOR     : str = "\x1b[J"
        SCREEN_PAST_CURSOR_ALT : str = "\x1b[0J"
        SCREEN_BEFORE_CURSOR   : str = "\x1b[1J"
        ALL                    : str = "\x1b[2J"
        SAVED_LINES            : str = "\x1b[3J"
        LINE_PAST_CURSOR       : str = "\x1b[K"
        LINE_PAST_CURSOR_ALT   : str = "\x1b[0K"
        LINE_BEFORE_CURSOR     : str = "\x1b[1K"
        LINE                   : str = "\x1b[2K"
        SAVE_SCREEN            : str = "\x1b[?47l"
        RESTORE_SCREEN         : str = "\x1b[?47h"

    STYLE: type[STYLES] = STYLES
    COLOR: type[COLORS] = COLORS
    COLOURS: type[COLORS] = COLORS
    COLOUR: type[COLORS] = COLORS
