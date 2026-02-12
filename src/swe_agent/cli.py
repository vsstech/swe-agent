from swe_agent.agent import run_agent

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without calling LLMs"
    )
    return parser.parse_args()

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--goal", required=True)
    args = parser.parse_args()

    state = run_agent(
        repo_path=args.repo_path,
        goal=args.goal
    )

    for obs in state.observations:
        print("-", obs)
