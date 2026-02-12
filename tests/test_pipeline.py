# tests/test_pipeline.py
from swe_agent.pipeline import analyze_repo


def test_analyze_repo_pipeline(tmp_path):
    # minimal repo
    repo = tmp_path / "repo"
    repo.mkdir()

    # source file
    (repo / "calc.py").write_text(
        "def add(a,b):\n"
        "    return a+b\n"
    )

    # tests
    tests_dir = repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_calc.py").write_text(
        "from calc import add\n\n"
        "def test_add():\n"
        "    assert add(1,2)==3\n"
    )

    reports = tmp_path / "reports"

    result = analyze_repo(str(repo), str(reports))

    assert "ruff" in result
    assert "coverage" in result
    assert "missing_tests" in result
    assert isinstance(result["missing_tests"], list)
