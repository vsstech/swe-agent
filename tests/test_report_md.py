from swe_agent.report_md import generate_markdown_report


def test_generate_markdown_report():
    report = {
        "repo_path": "demo",
        "ruff": {"returncode": 1, "stdout": "F401 unused import"},
        "coverage": {
            "files": [
                {"filename": "a.py", "coverage_percent": 50.0},
            ]
        },
        "missing_tests": [
            {
                "filename": "a.py",
                "function_name": "add",
                "suggestion": "Add test for edge cases",
            }
        ],
        "dependencies": {
            "outdated": [
                {"name": "requests", "current": "2.19.1", "latest": "2.32.0"}
            ],
            "vulnerable": [],
        },
    }

    md = generate_markdown_report(report)

    assert "# 🤖 SWE Agent Report" in md
    assert "requests" in md
    assert "add" in md
