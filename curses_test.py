import curses

def main(stdscr):
    curses.curs_set(0)
    for i in range(250):
        curses.init_pair(i+1, i, curses.COLOR_BLACK)
        stdscr.addstr(f"color {i}\t", curses.color_pair(i+1))
    stdscr.getch()

curses.wrapper(main)