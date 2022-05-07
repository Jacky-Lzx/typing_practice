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

    def add_text(self) -> None:
        self.lines = []
        with open("main.py", "r") as file_input:
            self.lines = file_input.readlines()

    def start(self, stdscr: curses.window) -> None:
        lines = self.lines
        window = self.window
        height, width = self.height, self.width

        text_pad = curses.newpad(len(lines) + 1, width - 2)

        outputs.append(f"len: {len(lines)}")

        for i, line in enumerate(lines):
            # text_pad.addstr(1 + i, 1, line)
            text_pad.addstr(line, curses.A_DIM |
                            curses.color_pair(self.WHITE_BLACK))

        stdscr.refresh()

        typed_lines = []

        line_index = 0
        column_index = 0
        ch = -1
        current_type_line = ""
        while True:
            window.border()
            window.addstr(0, 4, "Typing")
            window.addstr(0, 100, f"press: {ch}")
            window.refresh()

            text_pad.refresh(0, 0, 1, 1, height - 2, width - 2)

            ch = window.getch(1 + line_index, 1 + column_index)

            if ch == 4:  # Ctrl-D
                break

            if ch == 9:  # Tab
                continue

            if ch == ord(lines[line_index][column_index]):
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
                                       lines[line_index][column_index - 1], curses.A_DIM | self.WHITE_BLACK)
                        column_index -= 1
                        current_type_line = current_type_line[:-1]
                else:
                    text_pad.addch(line_index, column_index, ch,
                                   curses.A_BOLD | self.RED_BLACK)
                    column_index += 1
                    current_type_line += chr(ch)

            if column_index >= len(lines[line_index]):
                column_index = len(lines[line_index]) - 1

            if ch == 10:  # Enter
                # delete the new line character
                current_type_line = current_type_line[:-1]
                # draw the color for current line
                for i in range(len(lines[line_index])):
                    if i >= len(current_type_line):
                        text_pad.addch(line_index, i, lines[line_index][i],
                                       curses.A_DIM | self.RED_BLACK)
                        continue
                    if lines[line_index][i] != current_type_line[i]:
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

        outputs.append(typed_lines)


def main(stdscr: curses.window):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    window = stdscr.derwin(height, width, 0, 0)
    window.clear()

    typing_window = TypingWindow(window)
    typing_window.add_text()
    typing_window.start(stdscr)


wrapper(main)

print(outputs)
