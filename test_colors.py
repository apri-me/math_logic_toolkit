import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    for i in range(256):
        curses.init_pair(i+1, i, curses.COLOR_BLACK)
        stdscr.addstr(f"color-{i}\t", curses.color_pair(i+1))
    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)