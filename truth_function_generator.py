# NOTE: For a given formula, it just checks whether the number of right parens are equal to left parens.
def check_equality_of_paranthesis(formula):
    l = formula.count("(")
    r = formula.count(")")
    if l != r:
        raise NotEqualParanthesisException(
            f"The number of right and left paranthesis are not equal: {l} != {r}")


# NOTE: For a given string, it returns the index of outer paranthesis.
# e.g: "(A \and (B)) \or (C \and D)" -> [(0, 11), (17, 26)]
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


# NOTE: For a given formula it returns highest order schemes and connnectives.
# By highest order schemes we mean the schemes that aree in the outer paranthesis.
# e.g: in "(A \and (B \and C)) \or D", "(A \and (B \and C))" and "D" are highest order schemes but "(B \and C)" isn't.
# If the above example is given to function it returns -> ["(A \and (B \and C))", "\or", "D"]
def extract_highest_order_schemes_and_connectives(formula: str):
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


# NOTE: It gets the truth of some connective with some args by its truth bit.
# A truth bit is a 2^n string that shows every state of a connective. e.g for \or it's 0111.
def get_truth_by_truth_bit(args, truth_bit: str):
    truth_bit_idx = 0
    for i, arg in enumerate(args):
        efct = 2 ** (len(args) - i - 1)
        truth_bit_idx += efct * int(arg)
    return int(truth_bit[truth_bit_idx])


# NOTE: Gets a tape(highest order schemes and connectives) and returns just its connectives.
def get_tape_connectives(tape: list, connectives_dict: dict) -> list:
    return [s for s in tape if s in connectives_dict.keys()]


# NOTE: A formula can be in a badform. It means it can have more than one connectives in highest order tape.
# So it checks if this connectives can composite or not. e.g you can composite any number of \and s or \or s.
# But you can just write "a \imply b \imply c" or "a \and b \or c". If something like this happend it raise exceptions.
def check_allowed_composition(tape_cons: list, arg_no: int, connectives_dict: dict):
    first = tape_cons[0]
    for con in tape_cons:
        if not connectives_dict[con]['self_composite']:
            raise NotSelfCompositeConnective()
    else_comp_flag = False
    for con in tape_cons:
        if connectives_dict[con]['arg_no'] == arg_no and con != first:
            else_comp_flag = True
            break
    if not else_comp_flag:
        return
    for con in tape_cons:
        if not connectives_dict[con]['else_composite']:
            raise NotElseCompositeConnective()


# NOTE: If a tape has more than one connectives in highest order, we call it a bad-formed formula.
# We use this function to generates well-formed formula for a given bad-fromed formula.
# E.g it transforms this "a \and b \and c" to this "(a \and b) \and c"
# This makes computations easy.
def make_tape_well_formed(tape, connectives_dict):
    # NOTE: 3 is the maximum number of places that a connective has.
    for cn in range(3):
        tape_cons = get_tape_connectives(tape, connectives_dict)
        check_allowed_composition(tape_cons, cn, connectives_dict)
        if not tape_cons:
            if len(tape) == 1:
                break
            raise Exception(f"Out of connectives in higher order tape!{tape}")
        for con in tape_cons:
            if connectives_dict[con]['arg_no'] == cn:
                ind = tape.index(con)
                st = ind - cn // 2
                end = ind + (cn + 1) // 2 + 1
                s = " ".join(tape[st: end])
                s = f"({s})"
                tape[st: end] = [s]


# NOTE: It is a higher order function with Divide-and-Conquere approach that generates a truth function for a given formula.
# It is a recursive function that for base-case if the formula is just a variable it just returns a function..
# that returns the variable's value, and if not, with help of the tape of formula and functions that generated for lower order..
# formulas, it generates the truth function for the function by it's highest order connective and its truth-bit.
def generate_truth_function(formula: str, var_names: tuple[str], connectives_dict: dict):
    formula1 = formula.strip()
    if formula1.startswith("(") and formula1.endswith(")"):
        formula1 = formula1[1:-1].strip()
    if formula1 in var_names:
        return lambda *args: args[var_names.index(formula1)]
    tape = extract_highest_order_schemes_and_connectives(formula1)
    tape_cons = get_tape_connectives(tape, connectives_dict)
    if len(tape_cons) > 1:
        make_tape_well_formed(tape, connectives_dict)
        tape = extract_highest_order_schemes_and_connectives(tape[0][1:-1])
        tape_cons = get_tape_connectives(tape, connectives_dict)
    if not len(tape_cons) == 1:
        raise Exception(f"not well-formed! {len(tape_cons)}")
    con = tape_cons[0]
    tape.remove(con)
    tape_funcs = [generate_truth_function(
        a, var_names, connectives_dict) for a in tape]
    return lambda *args: get_truth_by_truth_bit([a(*args) for a in tape_funcs], connectives_dict[con]['truth_bit'])


class NotEqualParanthesisException(Exception):
    pass


class NotElseCompositeConnective(Exception):
    pass


class NotSelfCompositeConnective(Exception):
    pass
