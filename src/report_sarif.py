# src/report_sarif.py
import json
from typing import Dict, Any


def generate_sarif(report: Dict[str, Any]) -> Dict[str, Any]:
    results = []

    for s in report.get("missing_tests", []):
        results.append({
            "ruleId": "missing-unit-test",
            "message": {"text": s["suggestion"]},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": s["filename"]
                    }
                }
            }],
        })

    return {
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "SWE-Agent",
                    "rules": [{
                        "id": "missing-unit-test",
                        "name": "Missing unit test",
                    }],
                }
            },
            "results": results,
        }],
    }


def write_sarif(report: Dict[str, Any], path: str):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
