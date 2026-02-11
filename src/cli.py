from src.agent import run_agent


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--goal", required=True)
    args = parser.parse_args()

    state = run_agent(
        repo_path=args.repo_path,
        reports_dir="agent-reports",
        goal=args.goal,
    )

    for obs in state.observations:
        print("-", obs)
