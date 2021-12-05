def check_equality_of_paranthesis(formula):
    l = formula.count("(")
    r = formula.count(")")
    if l != r:
        raise NotEqualParanthesisException(
            f"The number of right and left paranthesis are not equal: {l} != {r}")


def find_parens(s):
    matchings = []
    pstack = []

    for i, c in enumerate(s):
        if c == '(':
            pstack.append(i)
        elif c == ')':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            elif len(pstack) == 1:
                matchings.append((pstack.pop(), i))
            else:
                pstack.pop()

    return matchings


def extract_highest_order_schemes_and_connectives(formula: str):
    """It returns a list that contains highest order schemes and connectives. 
This doesn't return any scheme, it just returns the parameter of the connective."""
    tape = []
    subschemes_idx = find_parens(formula)
    if subschemes_idx:
        s = formula[:subschemes_idx[0][0]].strip()
        if s:
            tape += s.split()
        for i, (start_idx, end_idx) in enumerate(subschemes_idx):
            tape.append(formula[start_idx: end_idx+1].strip())
            if i < len(subschemes_idx) - 1:
                tape.append(formula[end_idx+1: subschemes_idx[i+1][0]].strip())
            else:
                s = formula[end_idx+1:].strip()
                if s:
                    tape += s.split()
    else:
        tape += formula.strip().split()
    return tape


def get_truth_by_truth_bit(args, truth_bit: str):
    truth_bit_idx = 0
    for i, arg in enumerate(args):
        efct = 2 ** (len(args) - i - 1)
        truth_bit_idx += efct * int(arg)
    return truth_bit[truth_bit_idx]


def generate_truth_function(formula: str, var_names: tuple[str], connectives_dict: dict):
    """This function, generates a function that's work exactly like truth function of the formula.
formula is a well-formed formula in a string data and var_names is a set of variable names that may be used in formula."""
    formula1 = formula.strip()
    if formula1.startswith("(") and formula1.endswith(")"):
        formula1 = formula1[1:-1].strip()
    if formula1 in var_names:
        return lambda *args: args[var_names.index(formula1)]
    tape = extract_highest_order_schemes_and_connectives(formula1)
    tape_cons = [s for s in enumerate(tape) if s[1] in connectives_dict.keys()]
    if not len(tape_cons) == 1:
        raise Exception(f"not well-formed! {len(tape_cons)}")
    con = tape_cons[0]
    tape.remove(con[1])
    tape_funcs = [generate_truth_function(
        a, var_names, connectives_dict) for a in tape]
    return lambda *args: get_truth_by_truth_bit([a(*args) for a in tape_funcs], connectives_dict[con[1]]['truth_bit'])


class NotEqualParanthesisException(Exception):
    pass
