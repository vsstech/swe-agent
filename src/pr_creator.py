# src/pr_creator.py
from github import Github
from git import Repo
import os


def create_pr(
    repo_path: str,
    repo_full_name: str,
    branch_name: str,
    pr_title: str,
    pr_body: str,
):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set")

    # Git operations
    repo = Repo(repo_path)
    repo.git.checkout("-b", branch_name)
    repo.git.add(A=True)
    repo.index.commit(pr_title)

    origin = repo.remote(name="origin")
    origin.push(branch_name)

    # GitHub PR
    gh = Github(token)
    gh_repo = gh.get_repo(repo_full_name)

    pr = gh_repo.create_pull(
        title=pr_title,
        body=pr_body,
        head=branch_name,
        base="main",
    )

    return pr.html_url
