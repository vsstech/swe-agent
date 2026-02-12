# 1/test_coverage.py
from swe_agent.coverage import run_pytest_coverage,CoverageResult


def test_run_pytest_coverage_creates_xml(tmp_path):
    # create minimal python project
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    # src1 code
    (repo_dir / "calc.py").write_text(
        "def add(a,b):\n"
        "    return a+b\n"
    )

    # 1 folder
    tests_dir = repo_dir / "1"
    tests_dir.mkdir()
    (tests_dir / "test_calc.py").write_text(
        "from calc import add\n\n"
        "def test_add():\n"
        "    assert add(2,3)==5\n"
    )

    reports_dir = tmp_path / "reports"

    result = run_pytest_coverage(str(repo_dir), str(reports_dir))

    assert isinstance(result, CoverageResult)
    assert result.returncode == 0
    assert result.coverage_xml_path.endswith("coverage.xml")

    # coverage.xml should exist
    assert (reports_dir / "coverage.xml").exists()


def test_run_pytest_coverage_handles_failure(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    # broken test
    tests_dir = repo_dir / "1"
    tests_dir.mkdir()
    (tests_dir / "test_fail.py").write_text("def test_fail():\n    assert 1 == 2\n")

    reports_dir = tmp_path / "reports"

    result = run_pytest_coverage(str(repo_dir), str(reports_dir))

    assert result.returncode != 0
