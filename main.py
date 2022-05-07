from curses.textpad import Textbox, rectangle
import curses
from curses import wrapper
import enum
from sys import stderr

outputs = []

TAB_SIZE = 4


def main(stdscr: curses.window):

    WHITE_BLACK = 1
    GREEN_BLACK = 2
    RED_BLACK = 3
    curses.init_pair(WHITE_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()

    height, width = stdscr.getmaxyx()

    window = stdscr.derwin(height, width, 0, 0)
    window.clear()

    lines = []
    with open("main.py", "r") as file_input:
        lines = file_input.readlines()

    # text_pad = window.subpad(1, 1)
    # text_pad = curses.newpad(len(lines), max([len(a) for a in lines]) + 10)
    text_pad = curses.newpad(len(lines) + 1, width - 2)

    outputs.append(f"len: {len(lines)}")

    for i, line in enumerate(lines):
        # text_pad.addstr(1 + i, 1, line)
        text_pad.addstr(line, curses.A_DIM | curses.color_pair(WHITE_BLACK))

    stdscr.refresh()

    line_index = 0
    column_index = 0
    ch = -1
    while True:
        window.border()
        window.addstr(0, 4, "Title")
        window.addstr(0, 20, f"press: {ch}")
        window.refresh()

        text_pad.refresh(0, 0, 1, 1, height - 2, width - 2)

        ch = window.getch(1 + line_index, 1 + column_index)

        if ch == ord(lines[line_index][column_index]):
            text_pad.addch(line_index, column_index, ch,
                           curses.A_BOLD | curses.color_pair(GREEN_BLACK))
            column_index += 1
        else:
            if ch == 127:  # Backspace
                text_pad.addch(line_index, column_index - 1,
                               lines[line_index][column_index - 1], curses.A_DIM | curses.color_pair(WHITE_BLACK))
                column_index -= 1
            else:
                text_pad.addch(line_index, column_index, ch,
                               curses.A_BOLD | curses.color_pair(RED_BLACK))
                column_index += 1

        if column_index >= len(lines[line_index]):
            column_index = len(lines[line_index]) - 1

        if ch == 10:
            line_index += 1
            column_index = 0


wrapper(main)

print(outputs)
