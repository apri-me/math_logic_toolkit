from curses.textpad import Textbox, rectangle
import json
import curses
from math import floor

from truth_function_generator import generate_truth_function
from dcnf_gen import generate_cnf, generate_dnf
from truth_table_gen import gen_table


def get_input(stdscr, message, fw=1, fh=1):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, (w - len(message)) // 2, message)
    editwin_x, editwin_w = 3 + floor(w/2 * (1 - fw**(-1))), int(w // fw) - 6
    editwin_y, editwin_h = 4 + floor(h/2 * (1 - fh**(-1))), int(h // fh) - 8
    editwin = curses.newwin(editwin_h, editwin_w, editwin_y, editwin_x)
    rectangle(stdscr, editwin_y - 1, editwin_x - 1, h - editwin_y, w - editwin_x )
    box = Textbox(editwin)
    curses.curs_set(1)
    stdscr.refresh()
    box.edit()
    wff = box.gather()
    curses.curs_set(0)
    return wff.strip()


def get_wff_from_user(stdscr):
    return get_input(stdscr, "Enter your well-formed formula! hit (Ctrl-G) to save!", fw=1.2, fh=1.2)


def get_vars_from_user(stdscr):
    message = "Eneter varaiables that you want to use in formula. Seperate them by spaces then hit (Ctrl-G) to save!"
    return get_input(stdscr, message, fh=5, fw=2)


def get_connectives_dict(f="connectives.json"):
    with open("connectives.json") as f:
        connectives_dict = json.load(f)
    return connectives_dict


def print_menu(stdscr, menu_items, current_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for i, row in enumerate(menu_items):
        x = (w - len(row["name"])) // 2
        y = h // 2 - len(menu_items)//2 + i
        if i == current_row_idx:
            stdscr.attron(curses.color_pair(2))
        if not row["active"]:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(y, x, row["name"])
        if i == current_row_idx:
            stdscr.attroff(curses.color_pair(2))
        if not row["active"]:
            stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, 232, curses.COLOR_WHITE)
    curses.init_pair(3, 235, curses.COLOR_BLACK)
    current_wff = ""
    menu_items = [("ENTER WFF", True), ("TRUTH TABLE", False),
                  ("DNF", True), ("CNF", False), ("Quit", True)]
    menu_items = [
        {
            "name": "ENTER WFF",
            "active": True
        },
        {
            "name": "TRUTH TABLE",
            "active": False
        },
        {
            "name": "EQUIVALENT DNF",
            "active": False
        },
        {
            "name": "EQUIVALENT CNF",
            "active": False
        },
        {
            "name": "QUIT",
            "active": True
        },
    ]

    # curses.init_pair(3, )
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    connectives_dict = get_connectives_dict()
    vars = ("a", "b", "c")
    formula1 = "(\\neg a \\or b) \\imply c"

    f = generate_truth_function(formula1, vars, connectives_dict)

    table = gen_table(f, vars)

    print_menu(stdscr, menu_items, 0)

    current_row_idx = 0
    print_menu(stdscr, menu_items, current_row_idx)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP:
            current_row_idx -= 1
            current_row_idx %= len(menu_items)
            while not menu_items[current_row_idx]["active"]:
                current_row_idx -= 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_DOWN:
            current_row_idx += 1
            current_row_idx %= len(menu_items)
            while not menu_items[current_row_idx]["active"]:
                current_row_idx += 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row_idx]["name"] == "ENTER WFF":
                current_wff = get_vars_from_user(stdscr)
            stdscr.clear()
            stdscr.addstr(0, 0, "You pressed {}".format(
                menu_items[current_row_idx]["name"]))
            stdscr.refresh()
            stdscr.getch()

        print_menu(stdscr, menu_items, current_row_idx)

        stdscr.refresh()

    # vars = ("a", "b", "c")
    # formula1 = "(\\neg a \\or b) \\imply c"

    # f = generate_truth_function(formula1, vars, connectives_dict)

    # dnf = generate_dnf(f, vars, "\\and", "\\or", "\\neg")
    # cnf = generate_cnf(f, vars, "\\and", "\\or", "\\neg")
    # table= gen_table(f, vars)

    # print(dnf)
    # print(cnf)
    # print(table)


curses.wrapper(main)
