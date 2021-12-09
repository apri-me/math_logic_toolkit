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
    return int(truth_bit[truth_bit_idx])


def generate_truth_function(formula: str, var_names: tuple[str], connectives_dict: dict):
    """This function, generates a function that's work exactly like truth function of the formula.
formula is a well-formed formula in a string data and var_names is a set of variable names that may be used in formula."""
    formula1 = formula.strip()
    if formula1.startswith("(") and formula1.endswith(")"):
        formula1 = formula1[1:-1].strip()
    if formula1 in var_names:
        return lambda *args: args[var_names.index(formula1)]

    tape = extract_highest_order_schemes_and_connectives(formula1)
    # TODO: check for duplicate and self composition and else composition
    for i in range(len(tape)):
        if tape[i] not in connectives_dict.keys():
            tape[i] = generate_truth_function(tape[i], var_names, connectives_dict)

    y = None

    for cn in range(3): # NOTE: 3 is the maximum number of places that a connective has.
        tape_cons = [s for s in tape if s in connectives_dict.keys()]
        if not tape_cons:
            if len(tape) == 1:
                break
            raise Exception(f"Out of connectives in higher order tape!{tape}")
        for con in tape_cons:
            if connectives_dict[con]['arg_no'] == cn:
                ind = tape.index(con)
                st = ind - cn // 2
                end = ind + (cn + 1) // 2 + 1
                funcs = [f for f in tape[st: end] if f is not con]
                f = lambda *args: get_truth_by_truth_bit([func(*args) for func in funcs], connectives_dict[con]['truth_bit'])
                tape[st: end] = [f]
    return tape[0]


class NotEqualParanthesisException(Exception):
    pass
