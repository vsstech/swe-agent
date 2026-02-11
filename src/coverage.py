# swe_agent/coverage.py
from dataclasses import dataclass
import subprocess
import os


@dataclass
class CoverageResult:
    returncode: int
    stdout: str
    stderr: str
    coverage_xml_path: str


def run_pytest_coverage(repo_path: str, reports_dir: str) -> CoverageResult:
    os.makedirs(reports_dir, exist_ok=True)
    coverage_xml = os.path.join(reports_dir, "coverage.xml")

    p = subprocess.run(
        [
            "pytest",
            "-q",
            "--disable-warnings",
            "--maxfail=1",
            "--cov=.",
            f"--cov-report=xml:{coverage_xml}",
        ],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    return CoverageResult(
        returncode=p.returncode,
        stdout=p.stdout,
        stderr=p.stderr,
        coverage_xml_path=coverage_xml,
    )
