def generate_all_states(n):
    bit_strings = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
    return [[int(a) for a in s] for s in bit_strings]


def generate_states_and_output(n, truth_func):
    states = generate_all_states(n)
    return [[*state, truth_func(*state)] for state in states]


def generate_normal_form(truth_func, vars, basic_seperator, complex_seperator, neg_sym, out_base) -> str:
    n = len(vars)
    st_out = generate_states_and_output(n, truth_func)
    basics = []
    for so in st_out:
        if so[-1] == out_base:
            s = f" {basic_seperator} ".join([vars[i] if s else f"{neg_sym} {vars[i]}" for i, s in enumerate(so[:-1])])
            s = f"({s})"
            basics.append(s)
    out = f" {complex_seperator} ".join(basics)
    return f"({out})"


def generate_dnf(truth_func, vars, and_sym, or_sym, neg_sym):
    return generate_normal_form(truth_func, vars, and_sym, or_sym, neg_sym, 1)


def generate_cnf(truth_func, vars, and_sym, or_sym, neg_sym):
    return generate_normal_form(truth_func, vars, or_sym, and_sym, neg_sym, 0)