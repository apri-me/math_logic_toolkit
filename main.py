import json

from truth_function_generator import generate_truth_function
from dcnf_gen import generate_cnf, generate_dnf


vars = ("a", "b", "c")

formula1 = "(\\neg a \\or b) \\imply c"

with open("connectives.json") as f:
    connectives_dict = json.load(f)


f = generate_truth_function(formula1, vars, connectives_dict)


dnf = generate_dnf(f, vars, "\\and", "\\or", "\\neg")
cnf = generate_cnf(f, vars, "\\and", "\\or", "\\neg")

print(dnf)
print(cnf)
