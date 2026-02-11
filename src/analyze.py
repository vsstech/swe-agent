# src/analyze.py
from dataclasses import dataclass
import subprocess
from git import Repo
import tempfile
import os

@dataclass
class RuffResult:
    returncode: int
    stdout: str
    stderr: str


def clone_repo(repo_url: str, dest_dir: str) -> str:
    repo_path = os.path.join(dest_dir, "repo")
    Repo.clone_from(repo_url, repo_path)
    return repo_path


def run_ruff(repo_path: str) -> RuffResult:
    p = subprocess.run(
        ["ruff", "check", "."],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return RuffResult(
        returncode=p.returncode,
        stdout=p.stdout,
        stderr=p.stderr,
    )


def analyze_repo(repo_url: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        repo_path = clone_repo(repo_url, tmp)
        ruff_res = run_ruff(repo_path)

        return {
            "repo_url": repo_url,
            "ruff": {
                "returncode": ruff_res.returncode,
                "stdout": ruff_res.stdout,
                "stderr": ruff_res.stderr,
            },
        }
if __name__ == "__main__":
    print(analyze_repo("https://github.com/vsstech/sample_python_bad_repo"))
    print(analyze_repo("https://github.com/vsstech/swe_agent_repo2"))
