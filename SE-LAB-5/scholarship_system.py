
"""Screen scholarship applicants and save eligibility results."""

import ast
import json
import operator

results = {}
MERIT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800000
CUTOFF = 85

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculate_merit_score(gpa, extracurricular_credits):
    """Calculate merit using a restricted arithmetic formula."""
    expression = ast.parse(MERIT_FORMULA, mode="eval").body

    def evaluate(node):
        """Evaluate an allowed arithmetic expression."""
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.Name):
            if node.id == "gpa":
                return gpa
            if node.id == "credits":
                return extracurricular_credits
            raise ValueError("Unsupported formula variable.")

        if isinstance(node, ast.BinOp):
            operation = _BINARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported formula operator.")
            return operation(evaluate(node.left), evaluate(node.right))

        raise ValueError("Unsupported merit formula.")

    return evaluate(expression)


def evaluate_applicant(student_id, test_scores, logs=None):
    """Evaluate an applicant and record their score."""
    if logs is None:
        logs = []

    gpa = test_scores["gpa"]
    extracurricular_credits = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)
    score = calculate_merit_score(gpa, extracurricular_credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Update the merit scoring formula."""
    global MERIT_FORMULA

    previous_formula = MERIT_FORMULA
    MERIT_FORMULA = new_formula

    try:
        calculate_merit_score(1, 1)
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError):
        MERIT_FORMULA = previous_formula
        raise ValueError("Invalid merit formula.") from None


def persist_results(file="scholarships.json"):
    """Save applicant results to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=4)


def load_results(file="scholarships.json"):
    """Load applicant results from a JSON file."""
    global results

    try:
        with open(file, "r", encoding="utf-8") as input_file:
            results = json.load(input_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load results: {error}")


def print_shortlist():
    """Print eligible applicants and their scores."""
    print("Shortlisted applicants:")

    for student_id, applicant in results.items():
        if applicant["eligible"]:
            print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the scholarship screening program."""
    evaluate_applicant(
        "U001", {"gpa": 9.1, "credits": 4, "income": 450000}
    )
    evaluate_applicant(
        "U002", {"gpa": 7.2, "credits": 1, "income": 300000}
    )
    evaluate_applicant(
        "U003", {"gpa": 12.5, "credits": -3, "income": -1}
    )
    evaluate_applicant("U004", {"gpa": 6.5})

    formula = input("Merit formula (Enter to keep default): ")

    if formula:
        try:
            change_formula(formula)
        except ValueError as error:
            print(error)
            return

    evaluate_applicant(
        "U005", {"gpa": 8.4, "credits": 3, "income": 600000}
    )
    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
