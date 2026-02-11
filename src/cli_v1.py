# src/cli_v1.py
import argparse
import json
import os

from src.pipeline import analyze_repo
from src.report_md import generate_markdown_report


def main():
    parser = argparse.ArgumentParser(description="SWE Agent")
    parser.add_argument("repo_path")
    parser.add_argument("--reports-dir", default="agent-reports")
    parser.add_argument("--generate-tests", action="store_true")

    args = parser.parse_args()

    report = analyze_repo(
        repo_path=args.repo_path,
        reports_dir=args.reports_dir,
        generate_tests=args.generate_tests,
    )

    os.makedirs(args.reports_dir, exist_ok=True)

    with open(os.path.join(args.reports_dir, "report.json"), "w") as f:
        json.dump(report, f, indent=2)

    md = generate_markdown_report(report)
    with open(os.path.join(args.reports_dir, "report.md"), "w") as f:
        f.write(md)

    print("SWE Agent analysis complete")


if __name__ == "__main__":
    main()
