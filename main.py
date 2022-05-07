from curses.textpad import Textbox, rectangle
import curses
from curses import wrapper
import enum
from sys import stderr

outputs = []

TAB_SIZE = 4


class TypingWindow:
    def __init__(self, window: curses.window) -> None:
        self.window = window
        self.height, self.width = window.getmaxyx()

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.WHITE_BLACK = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.GREEN_BLACK = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.RED_BLACK = curses.color_pair(3)

    def add_text(self, file_path: str) -> None:
        self.lines = []
        with open(file_path, "r") as file_input:
            self.lines = file_input.readlines()

        # remove '\n' in the end of each line
        for i, line in enumerate(self.lines):
            self.lines[i] = line[:-1]

    def start(self, stdscr: curses.window) -> None:
        lines = self.lines
        window = self.window
        height, width = self.height, self.width

        text_pad = curses.newpad(1000, width - 2)

        outputs.append(f"len: {len(lines)}")

        for i, line in enumerate(lines):
            # text_pad.addstr(1 + i, 1, line)
            text_pad.addstr(line + "\n", curses.A_DIM |
                            curses.color_pair(self.WHITE_BLACK))

        stdscr.refresh()

        typed_lines = []

        line_index = 0
        column_index = 0
        ch = -1
        current_type_line = ""
        current_line = lines[line_index]
        while True:
            window.border()
            window.addstr(0, 4, "Typing")
            window.addstr(0, width - 20, f"press: {ch}")
            window.refresh()

            text_pad.refresh(0, 0, 1, 1, height - 2, width - 2)

            ch = window.getch(1 + line_index, 1 + column_index)

            if ch == 4:  # Ctrl-D
                break
            elif ch == 9:  # Tab
                continue
            elif ch == 10:  # Enter
                # draw the color for current line
                for i in range(len(current_line)):
                    if i >= len(current_type_line):
                        text_pad.addch(line_index, i, current_line[i],
                                       curses.A_DIM | self.RED_BLACK)
                        continue
                    if current_line[i] != current_type_line[i]:
                        # draw red color
                        text_pad.addch(line_index, i, current_type_line[i],
                                       curses.A_BOLD | self.RED_BLACK)
                    else:
                        # draw green color
                        text_pad.addch(line_index, i, current_type_line[i],
                                       curses.A_BOLD | self.GREEN_BLACK)

                line_index += 1
                column_index = 0
                typed_lines.append(current_type_line)
                current_type_line = ""
                current_line = lines[line_index]
                continue
            elif ch == 127:  # Backspace
                if len(current_type_line) == 0:
                    pass
                else:
                    text_pad.addch(line_index, column_index - 1,
                                   current_line[column_index - 1], curses.A_DIM | self.WHITE_BLACK)
                    column_index -= 1
                    current_type_line = current_type_line[:-1]
                continue

            if column_index >= len(current_line):
                continue

            if ch == ord(current_line[column_index]):
                text_pad.addch(line_index, column_index, ch,
                               curses.A_BOLD | self.GREEN_BLACK)
                column_index += 1
                current_type_line += chr(ch)
            else:
                if ch == 127:  # Backspace
                    if len(current_type_line) == 0:
                        pass
                    else:
                        text_pad.addch(line_index, column_index - 1,
                                       current_line[column_index - 1], curses.A_DIM | self.WHITE_BLACK)
                        column_index -= 1
                        current_type_line = current_type_line[:-1]
                else:
                    text_pad.addch(line_index, column_index, ch,
                                   curses.A_BOLD | self.RED_BLACK)
                    column_index += 1
                    current_type_line += chr(ch)

        outputs.append(typed_lines)


def main(stdscr: curses.window):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    window = stdscr.derwin(height, width, 0, 0)
    window.clear()

    typing_window = TypingWindow(window)
    typing_window.add_text("main.py")
    typing_window.start(stdscr)


wrapper(main)

print(outputs)
