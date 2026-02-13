# swe_agent/tool_executor.py
import os
from swe_agent.analyze import run_ruff
from swe_agent.code_coverage import run_pytest_coverage
from swe_agent.coverage_parser import parse_coverage_xml
from swe_agent.dependencies import find_outdated_dependencies, find_vulnerable_dependencies
from swe_agent.report_md import generate_markdown_report, write_markdown_report
from swe_agent.report_sarif import generate_sarif, write_sarif
from swe_agent.test_suggester import suggest_tests_for_file
from swe_agent.test_generation_pipeline import generate_test_file


def execute_action(state, action: str):
    repo = state.repo_path
    reports = state.reports_dir

    if action == "run_lint":
        print(f"Running lint: {action}")
        res = run_ruff(repo)
        print(f"Completed Running lint: {action}")
        state.observations.append(f"Ruff exit code: {res.returncode}")

    elif action == "run_tests":
        res = run_pytest_coverage(repo, reports)
        state.report["coverage_raw"] = res.coverage_xml_path
        state.observations.append(f"Pytest exit code: {res.returncode}")

    elif action == "analyze_coverage":
        xml = state.report.get("coverage_raw")
        if not xml or not os.path.exists(xml):
            state.observations.append("No coverage data available")
            return

        files = parse_coverage_xml(xml)
        state.report["coverage_files"] = [f.__dict__ for f in files]

        avg = sum(f.coverage_percent for f in files) / len(files)
        state.coverage_percent = round(avg, 2)

        state.observations.append(f"Average coverage: {state.coverage_percent}%")

    elif action == "generate_tests":
        low_coverage = [
            f for f in state.report.get("coverage_files", [])
            if f["coverage_percent"] < 80
        ]

        for f in low_coverage:
            path = os.path.join(repo, f["filename"])
            suggestions = suggest_tests_for_file(path)
            generate_test_file(
                source_file=path,
                suggestions=[s.suggestion for s in suggestions],
                tests_dir=os.path.join(repo, "tests"),
            )

        state.tests_generated = True
        state.observations.append("Generated unit tests")

    elif action == "create_pr":
        state.observations.append("PR creation requested")

    elif action == "dependency_analysis":
        state.report["dependencies"] = {
            "outdated": [d.__dict__ for d in find_outdated_dependencies(state.repo_path)],
            "vulnerable": [v.__dict__ for v in find_vulnerable_dependencies(state.repo_path)],
        }
        state.observations.append("Completed Dependency analysis")

    elif action == "write_report":
        md = generate_markdown_report(state.report)
        write_markdown_report(md, os.path.join(state.reports_dir, "report.md"))

        sarif = generate_sarif(state.report)
        write_sarif(sarif, os.path.join(state.reports_dir, "report.sarif"))
    elif action == "stop":
        state.observations.append("Agent stopped")

    else:
        raise ValueError(f"Unknown action: {action}")

