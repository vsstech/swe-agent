# src/test_suggester.py
import ast
from dataclasses import dataclass
from typing import List


@dataclass
class TestSuggestion:
    filename: str
    function_name: str
    suggestion: str


def suggest_tests_for_file(file_path: str) -> List[TestSuggestion]:
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    suggestions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            fn = node.name

            # Simple heuristics
            if fn.startswith("_"):
                continue

            if fn.startswith(("get", "fetch", "load")):
                msg = "Add test for normal return value and empty result"

            elif fn.startswith(("create", "add")):
                msg = "Add test for valid input and invalid input"

            elif fn.startswith(("delete", "remove")):
                msg = "Add test for existing and non-existing item"

            else:
                msg = "Add test for happy path and edge cases"

            suggestions.append(
                TestSuggestion(
                    filename=file_path,
                    function_name=fn,
                    suggestion=msg,
                )
            )

    return suggestions
