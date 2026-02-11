# 1/test_analyze.py
from src.analyze import RuffResult,run_ruff


def test_run_ruff_returns_result(tmp_path):
    # create a tiny python file with a lint issue
    code_dir = tmp_path / "repo"
    code_dir.mkdir()
    (code_dir / "bad.py").write_text("import os\n\nx=1\n")

    result = run_ruff(str(code_dir))

    assert isinstance(result, RuffResult)
    assert result.returncode in (0, 1)   # 0 if no issues, 1 if issues
    assert isinstance(result.stdout, str)
    assert isinstance(result.stderr, str)


def test_run_ruff_fails_on_missing_path():
    result = run_ruff("/this/path/does/not/exist")
    assert result.returncode != 0
