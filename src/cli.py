from src.agent import run_agent

def main():
    state = run_agent(
        repo_path=".",
        reports_dir="agent-reports",
        goal="Improve test coverage to at least 80% without changing production code",
    )

    print("Actions taken:", state.actions_taken)
    print("Observations:")
    for o in state.observations:
        print("-", o)
