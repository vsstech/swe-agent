# src/agent.py
from dataclasses import dataclass
from typing import List, Dict, Any

from src.planner import plan_next_action
from src.pipeline import analyze_repo

MAX_STEPS = 5

@dataclass
class AgentState:
    goal: str
    observations: List[str]
    actions_taken: List[str]
    report: Dict[str, Any]


def run_agent(repo_path: str, goal: str):
    state = AgentState(
        goal=goal,
        observations=[],
        actions_taken=[],
        report={},
    )

    for _ in range(MAX_STEPS):
        action = plan_next_action(state.goal, state.observations)
        state.actions_taken.append(action)

        if action == "stop":
            break

        if action == "run_tests":
            state.report = analyze_repo(repo_path, "agent-reports")
            cov = state.report.get("coverage", {})
            state.observations.append(f"Coverage: {cov}")

        elif action == "generate_tests":
            state.observations.append("Generated unit tests")

        elif action == "create_pr":
            state.observations.append("PR created")

        else:
            state.observations.append(f"Action {action} executed")

    return state



