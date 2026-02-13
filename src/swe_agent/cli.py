from swe_agent.agent import run_agent

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--goal", required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    state = run_agent(
        repo_path = args.repo_path,
        reports_dir="agent-reports",
        goal=args.goal
    )
    print("Actions taken:", state.actions_taken)
    print("Observations:")
    for obs in state.observations:
        print("-", obs)
