from swe_agent.pr_creator import create_pr
import os
import pytest


def test_pr_creator_requires_token():
    if "GITHUB_TOKEN" in os.environ:
        del os.environ["GITHUB_TOKEN"]

    with pytest.raises(RuntimeError):
        create_pr(
            repo_path=".",
            repo_full_name="user/repo",
            branch_name="test",
            pr_title="test",
            pr_body="test",
        )
