# tests/test_test_suggester.py
from src.test_suggester import suggest_tests_for_file


def test_suggest_tests_for_file(tmp_path):
    py = tmp_path / "service.py"
    py.write_text(
        """
def create_user(name):
    return {"name": name}

def delete_user(uid):
    pass

def risky_logic(x):
    return x * 2
"""
    )

    suggestions = suggest_tests_for_file(str(py))

    assert len(suggestions) == 3

    names = {s.function_name for s in suggestions}
    assert "create_user" in names
    assert "delete_user" in names
    assert "risky_logic" in names

    create_msg = [s.suggestion for s in suggestions if s.function_name == "create_user"][0]
    assert "valid input" in create_msg.lower()
