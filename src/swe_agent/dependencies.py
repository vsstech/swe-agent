# src/dependencies.py
import subprocess
from dataclasses import dataclass
from typing import List


@dataclass
class OutdatedDependency:
    name: str
    current: str
    latest: str


@dataclass
class VulnerableDependency:
    name: str
    version: str
    advisory: str


def find_outdated_dependencies(repo_path: str) -> List[OutdatedDependency]:
    p = subprocess.run(
        ["pip", "list", "--outdated", "--format=json"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if p.returncode != 0 or not p.stdout:
        return []

    import json
    data = json.loads(p.stdout)

    return [
        OutdatedDependency(
            name=d["name"],
            current=d["version"],
            latest=d["latest_version"],
        )
        for d in data
    ]


def find_vulnerable_dependencies(repo_path: str) -> List[VulnerableDependency]:
    p = subprocess.run(
        ["pip-audit", "--format", "json"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if p.returncode != 0 or not p.stdout:
        return []

    import json
    data = json.loads(p.stdout)

    vulns = []
    for dep in data.get("dependencies", []):
        for v in dep.get("vulns", []):
            vulns.append(
                VulnerableDependency(
                    name=dep["name"],
                    version=dep["version"],
                    advisory=v.get("id", "unknown"),
                )
            )
    return vulns
