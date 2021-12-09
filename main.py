import json

from truth_function_generator import generate_truth_function


def generate_all_states(n):
    bit_strings = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
    return [[int(a) for a in s] for s in bit_strings]



vars = ("a", "b", "c")
formula = "((\\neg a) \\or b) \\imply c"
formula2 = "(a \\and b \\and c)"
formula3 = "\\neg a \\and b"

formula4 = "\\neg a"

with open("connectives.json") as f:
    connectives_dict = json.load(f)

f = generate_truth_function(formula2, vars, connectives_dict)

states = generate_all_states(3)
for st in states:
    print(f"{st}:\t {f(*st)}")



# f = generate_truth_function(formula4, vars, connectives_dict)