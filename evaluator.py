from pyparsing import *
import ast


def Add(left, right):
    return int(left + right)


def Subtract(left, right):
    return int(left - right)


def Multiply(left, right):
    return int(left * right)


def Divide(left, right):
    return int(left / right)


def Power(left, right):
    return int(left**right)


def pemdas_eval(expression):
    print(f"expression: {expression}")
    # Parse the expression into an abstract syntax tree
    parsed = ast.parse(expression, mode="eval")

    # Define a dictionary of allowed operators
    operators = {
        "Add": Add,
        "Sub": Subtract,
        "Mult": Multiply,
        "Div": Divide,
        "Pow": Power,
    }

    # Define a function that recursively evaluates the tree nodes
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            op = operators[type(node.op).__name__]
            return op(left=left, right=right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)
            op = type(node.op)
            if op == ast.UAdd:
                return +operand
            elif op == ast.USub:
                return -operand

        if isinstance(node, ast.Name):
            raise NameError(f"Name '{node.id}' is not defined")

        raise TypeError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the tree and return the result
    return evaluate(parsed)


# define the grammar for arithmetic expressions
integer = pyparsing_common.integer()
real = pyparsing_common.real()
number = real | integer
variable = Word(alphas, exact=1) + Word(nums)
operand = number | variable
operator = oneOf("+ - * / **").set_results_name("operator")
expr = infixNotation(
    operand,
    [
        (operator, 2, opAssoc.LEFT),
    ],
)


def parse(string):
    string = string.strip().upper()
    string = " ".join(string.split())

    if not string:
        return string

    try:
        return expr.parseString(string, parse_all=True)
    except ParseException:
        return "error"


# test the parser with a sample string
test_string = """2 ** 2
1+1
7 + 2 * 4
(7 + 2) * 4
A1 + A2
A1 * A2
MIN(A1:A4)
AVG(A1:A4)
2 * 3 + x1 - 4
""".split(
    "\n"
)

alphabet = set(letter for letter in alphas.upper())


def evaluate_tokens(tokens, session_state):
    if tokens == "error":
        return tokens
    elif not tokens:
        return tokens

    evaluation = []

    variable_letter = ""
    evaluate_variable = False

    for token in tokens:
        # we always expect variable to be LETTER + NUMBER
        # and only one letter and number
        if evaluate_variable:
            number = token
            cell_reference = session_state[f"{variable_letter}{number}"]

            # if cell is blank, make it zero
            if not cell_reference:
                cell_reference == "0"

            evaluation.append(str(evaluate_tokens(cell_reference, session_state)))
            evaluate_variable = False
            continue

        if hasattr(token, "_all_names"):
            evaluation.append(str(evaluate_tokens(token, session_state)))
        else:
            if token in alphabet:
                variable_letter = token
                evaluate_variable = True
                continue
            else:
                evaluation.append(str(token))

    string_to_evaluate = " ".join(evaluation)

    if string_to_evaluate != "e r r o r":
        result = pemdas_eval(string_to_evaluate)

    return result


def parse_and_evaluate(string, session_state):
    tokens = parse(string)
    return evaluate_tokens(tokens, session_state)

if __name__ == "__main__":
    session_state = {"A1": "2", "A2": "4"}
    result = parse_and_evaluate("2 + A1", session_state)
    print(result)
    print("HI")
