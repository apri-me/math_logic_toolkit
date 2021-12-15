import curses
from prettytable import PrettyTable

def main(stdscr):
    stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    pt = PrettyTable(["S1", "S2"])
    pt.add_row([1, 2])
    pt.add_row([3, 4])
    stdscr.addstr(10, 10, str(pt))

    stdscr.getch()


curses.wrapper(main)