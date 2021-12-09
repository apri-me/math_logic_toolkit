from dcnf_gen import generate_states_and_output

from prettytable import PrettyTable as PT


def gen_table(truth_func, vars):
    n = len(vars)
    st_out = generate_states_and_output(n, truth_func)
    pt = PT([*vars, "OUTPUT"])
    for st in st_out:
        pt.add_row(["T" if s else "F" for s in st])
    return pt