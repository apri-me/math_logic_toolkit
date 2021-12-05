import json

from truth_function_generator import generate_truth_function


def main():
    vars = ("a", "b", "c")
    formula = "((\\neg a) \\or b) \\imply c"

    with open("connectives.json") as f:
        connectives_dict = json.load(f)

    truth_func = generate_truth_function(formula, vars, connectives_dict)
    print(truth_func(0, 1, 1))




if __name__ == "__main__":
    main()
