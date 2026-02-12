# tests/test_dependencies.py
from swe_agent.dependencies import find_outdated_dependencies, find_vulnerable_dependencies
import subprocess
import json


class DummyCompleted:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def test_find_outdated_dependencies(monkeypatch):
    fake_output = json.dumps([
        {
            "name": "requests",
            "version": "2.19.1",
            "latest_version": "2.32.0",
        }
    ])

    def fake_run(*args, **kwargs):
        return DummyCompleted(stdout=fake_output)

    monkeypatch.setattr(subprocess, "run", fake_run)

    deps = find_outdated_dependencies(".")

    assert len(deps) == 1
    assert deps[0].name == "requests"
    assert deps[0].current == "2.19.1"


def test_find_vulnerable_dependencies(monkeypatch):
    fake_output = json.dumps({
        "dependencies": [
            {
                "name": "flask",
                "version": "1.0",
                "vulns": [{"id": "CVE-XXXX"}],
            }
        ]
    })

    def fake_run(*args, **kwargs):
        return DummyCompleted(stdout=fake_output)

    monkeypatch.setattr(subprocess, "run", fake_run)

    vulns = find_vulnerable_dependencies(".")

    assert len(vulns) == 1
    assert vulns[0].name == "flask"
    assert vulns[0].advisory == "CVE-XXXX"
