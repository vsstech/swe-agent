# src/report_md.py
from typing import Dict, Any
from datetime import datetime


def generate_markdown_report(report: Dict[str, Any]) -> str:
    lines = []

    lines.append("# 🤖 SWE Agent Report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()} UTC")
    lines.append("")
    lines.append(f"Repository: `{report['repo_path']}`")
    lines.append("")

    # Ruff
    lines.append("## 🔍 Lint Analysis (Ruff)")
    ruff = report.get("ruff", {})
    lines.append(f"- Exit code: `{ruff.get('returncode')}`")
    if ruff.get("stdout"):
        lines.append("```")
        lines.append(ruff["stdout"])
        lines.append("```")

    # Coverage
    lines.append("## 🧪 Test Coverage")
    files = report.get("coverage", {}).get("files", [])
    if files:
        lines.append("| File | Coverage |")
        lines.append("|------|----------|")
        for f in files:
            lines.append(f"| `{f['filename']}` | {f['coverage_percent']}% |")
    else:
        lines.append("_No coverage data available_")

    # Missing tests
    lines.append("## 🧩 Suggested Unit Tests")
    missing = report.get("missing_tests", [])
    if missing:
        for s in missing:
            lines.append(
                f"- `{s['filename']}` → `{s['function_name']}`: {s['suggestion']}"
            )
    else:
        lines.append("_No missing tests detected_")

    # Dependencies
    deps = report.get("dependencies", {})
    lines.append("## 📦 Dependencies")

    outdated = deps.get("outdated", [])
    if outdated:
        lines.append("### Outdated")
        for d in outdated:
            lines.append(
                f"- `{d['name']}`: {d['current']} → {d['latest']}"
            )

    vulnerable = deps.get("vulnerable", [])
    if vulnerable:
        lines.append("### Vulnerabilities")
        for v in vulnerable:
            lines.append(
                f"- `{v['name']} {v['version']}`: {v['advisory']}"
            )

    return "\n".join(lines)

def write_markdown_report(md: str, path: str):
    with open(path, "w") as f:
        f.write(md)
