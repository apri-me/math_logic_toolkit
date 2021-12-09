import json

from truth_function_generator import generate_truth_function


vars = ("a", "b")
formula = "((\\neg a) \\or b) \\imply c"
formula2 = "(a \\and b \\and c)"
formula3 = "\\neg a \\and b"

formula4 = "\\neg a"

with open("connectives.json") as f:
    connectives_dict = json.load(f)

# truth_func = generate_truth_function(formula2, vars, connectives_dict)
# print(truth_func(1, 1, 1))
# a, _, b, _, c = generate_truth_function(formula2, vars, connectives_dict)

nega = generate_truth_function(formula3, vars, connectives_dict)

# f = generate_truth_function(formula4, vars, connectives_dict)