import json
import curses

from truth_function_generator import generate_truth_function
from dcnf_gen import generate_cnf, generate_dnf
from truth_table_gen import gen_table

def get_connectives_dict(f="connectives.json"):
    with open("connectives.json") as f:
        connectives_dict = json.load(f)
    return connectives_dict


def print_menu(stdscr, menu_items, current_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for i, row in enumerate(menu_items):
        x = (w - len(row[0])) // 2
        y = h // 2  -  len(menu_items)//2 + i
        if i == current_row_idx:
            stdscr.attron(curses.color_pair(2))
        if row[1] is False:
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(y, x, row[0])
        if i == current_row_idx:
            stdscr.attroff(curses.color_pair(2))
        if row[1] is False:
            stdscr.attroff(curses.color_pair(3))
        
    
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, 232, curses.COLOR_WHITE)
    curses.init_pair(3, 235, curses.COLOR_BLACK)
    menu_items = [("ENTER WFF", True), ("TRUTH TABLE", False), ("DNF", True), ("CNF", False), ("Quit", True)]

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
            while not menu_items[current_row_idx][1]:
                current_row_idx -= 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_DOWN:
            current_row_idx += 1
            current_row_idx %= len(menu_items)
            while not menu_items[current_row_idx][1]:
                current_row_idx += 1
                current_row_idx %= len(menu_items)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.addstr(0, 0, "You pressed {}".format(menu_items[current_row_idx][0]))
            stdscr.refresh()
            stdscr.getch()
            if menu_items[current_row_idx][0] == 'Quit':
                break
        elif key == ord('q'):
            break

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