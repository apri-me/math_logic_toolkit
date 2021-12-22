from curses.textpad import Textbox, rectangle
import json
import curses
from math import floor

from truth_function_generator import generate_truth_function
from dcnf_gen import generate_cnf, generate_dnf
from truth_table_gen import gen_table


def add_new_lines_to_nf(stdscr, nf: str):
    _, w = stdscr.getmaxyx()
    if len(nf) > w - 2:
        ind = nf[:w-2].rfind("(")
        return nf[:ind] + "\n" + add_new_lines_to_nf(stdscr, nf[ind:])
    return nf


def centralized_yx(stdscr, text):
    lines_no = text.count("\n") + 1
    firstl = text.splitlines()[0]
    h, w = stdscr.getmaxyx()
    x = (w - len(firstl)) // 2
    y = (h - lines_no) // 2
    return y, x, lines_no


def multi_addstr(stdscr, y, x, message: str, color_pair):
    for i, line in enumerate(message.splitlines()):
        stdscr.addstr(y+i, x, line, color_pair)


def w84q(stdscr):
    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            break


def get_input(stdscr, message, fw=1, fh=1, default=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, (w - len(message)) // 2, message, curses.color_pair(6))
    editwin_x, editwin_w = 3 + floor(w/2 * (1 - fw**(-1))), int(w // fw) - 6
    editwin_y, editwin_h = 4 + floor(h/2 * (1 - fh**(-1))), int(h // fh) - 8
    editwin = curses.newwin(editwin_h, editwin_w, editwin_y, editwin_x)
    rectangle(stdscr, editwin_y - 1, editwin_x -
              1, h - editwin_y, w - editwin_x)
    box = Textbox(editwin)
    curses.curs_set(1)
    stdscr.refresh()
    curses.beep()
    editwin.addstr(default.encode("utf-8"))
    box.edit()
    wff = box.gather()
    curses.curs_set(0)
    return wff.strip()


def get_wff_from_user(stdscr, default):
    message = "Enter your well-formed formula! hit (Ctrl-G) to save!"
    return get_input(stdscr, message, fw=1.2, fh=1.2, default=default)


def get_vars_from_user(stdscr, default):
    message = "Eneter varaiables that you want to use in formula. Seperate them by spaces then hit (Ctrl-G) to save!"
    return get_input(stdscr, message, fh=3, fw=2, default=default)


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
        if not row["active"]():
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(y, x, row["name"])
        if i == current_row_idx:
            stdscr.attroff(curses.color_pair(2))
        if not row["active"]():
            stdscr.attroff(curses.color_pair(3))

    stdscr.refresh()


def print_help_menu(stdscr, connectives_dict: dict):
    _, x = stdscr.getmaxyx()
    main_message = "We use latex-like commands for connectives."
    stdscr.addstr(1, (x - len(main_message))//2, main_message, curses.color_pair(5))
    truth_bit_message = "Truth-bit is 2^n-bit string that shows connective's behaviour in each state."
    stdscr.addstr(3, (x - len(truth_bit_message))//2, truth_bit_message, curses.color_pair(5))
    connectives_title = "You can see all connectives command below"
    stdscr.addstr(5, (x - len(connectives_title))//2, connectives_title)
    for i, (con, di) in enumerate(connectives_dict.items()):
        text = f"{con} for {di['name']}"
        length = len(text)
        text = text.split()
        stdscr.addstr(6+i, (x - length)//2, text[0], curses.color_pair(6))
        stdscr.addstr(f" {text[1]} ")
        stdscr.addstr(" ".join(text[2:]), curses.color_pair(4))
    examples = [
        "(a \\and b \\and c)",
        "(a \\nand b) \\imply \\bot",
        "(p \\or \\neg q) \\imply (p \\or q)"
    ]
    start_ind = i + 12
    example_title = "These are some examples of formulas:"
    stdscr.addstr(start_ind-2, (x - len(example_title))//2, example_title, curses.color_pair(5))
    for i, eg in enumerate(examples):
        stdscr.addstr(start_ind+2*i, (x - len(eg))//2, eg, curses.color_pair(6))
    start_ind += 2*i + 4
    quite_message = "Enter q to quite menu!"
    stdscr.addstr(start_ind, (x - len(quite_message))//2, quite_message, curses.color_pair(4))



def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, 75, curses.COLOR_BLACK) # Main color: Light Blue
    curses.init_pair(2, 232, curses.COLOR_WHITE) # Selected item: background White
    curses.init_pair(3, 235, curses.COLOR_BLACK) # Disabled item: gray near to black
    curses.init_pair(4, 160, curses.COLOR_BLACK) # errored text: red
    curses.init_pair(5, 220, curses.COLOR_BLACK) # Warned text: yello
    curses.init_pair(6, 40, curses.COLOR_BLACK) # Succeeded text: green

    current_wff = ""
    truth_function = None
    menu_items = [("ENTER WFF", True), ("TRUTH TABLE", False),
                  ("DNF", True), ("CNF", False), ("Quit", True)]
    menu_items = [
        {
            "name": "ENTER WFF",
            "active": lambda : True
        },
        {
            "name": "TRUTH TABLE",
            "active": lambda : bool(current_wff)
        },
        {
            "name": "EQUIVALENT DNF",
            "active": lambda : bool(current_wff)
        },
        {
            "name": "EQUIVALENT CNF",
            "active": lambda : bool(current_wff)
        },
        {
            "name": "HELP",
            "active": lambda : True
        },
        {
            "name": "QUIT",
            "active": lambda : True
        },
    ]

    # curses.init_pair(3, )
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    connectives_dict = get_connectives_dict()
    vars = []
    print_menu(stdscr, menu_items, 0)
    current_row_idx = 0
    print_menu(stdscr, menu_items, current_row_idx)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP:
            current_row_idx -= 1
            current_row_idx %= len(menu_items)
            while not menu_items[current_row_idx]["active"]():
                current_row_idx -= 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_DOWN:
            current_row_idx += 1
            current_row_idx %= len(menu_items)
            while not menu_items[current_row_idx]["active"]():
                current_row_idx += 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row_idx]["name"] == "ENTER WFF":
                vars = get_vars_from_user(
                    stdscr, default=" ".join(vars)).strip().split()
                current_wff = get_wff_from_user(stdscr, default=current_wff)
                truth_function = generate_truth_function(
                    current_wff, vars, connectives_dict)
            elif menu_items[current_row_idx]["name"] == "TRUTH TABLE":
                stdscr.clear()
                table = gen_table(truth_function, vars)
                y, x, lines_no = centralized_yx(stdscr, table)
                multi_addstr(stdscr, y, x, table, curses.color_pair(5))
                quite_message = "Press 'q' to quite table!"
                stdscr.addstr(y+lines_no, x, quite_message, curses.color_pair(4))
                w84q(stdscr)

            elif menu_items[current_row_idx]["name"] == "EQUIVALENT DNF":
                dnf = generate_dnf(truth_function, vars,
                                   "\\and", "\\or", "\\neg")
                dnf = add_new_lines_to_nf(stdscr, dnf)
                y, x, lines_no = centralized_yx(stdscr, dnf)
                multi_addstr(stdscr, y, x, dnf, curses.color_pair(5))
                quite_message = "Press 'q' to quite dnf!"
                stdscr.addstr(y+lines_no+1, x, quite_message, curses.color_pair(4))
                w84q(stdscr)
            elif menu_items[current_row_idx]["name"] == "EQUIVALENT CNF":
                cnf = generate_cnf(truth_function, vars,
                                   "\\and", "\\or", "\\neg")
                cnf = add_new_lines_to_nf(stdscr, cnf)
                y, x, lines_no = centralized_yx(stdscr, cnf)
                multi_addstr(stdscr, y, x, cnf, curses.color_pair(5))
                quite_message = "Press 'q' to quite cnf!"
                stdscr.addstr(y+lines_no+1, x, quite_message, curses.color_pair(4))
                w84q(stdscr)
            
            elif menu_items[current_row_idx]["name"] == "HELP":
                print_help_menu(stdscr, connectives_dict)
                w84q(stdscr)

            elif menu_items[current_row_idx]["name"] == "QUIT":
                return

        print_menu(stdscr, menu_items, current_row_idx)
        stdscr.refresh()


curses.wrapper(main)