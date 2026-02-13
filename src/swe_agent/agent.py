# src/agent.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

from swe_agent.planner import plan_next_action
from swe_agent.tool_executor import execute_action
MAX_STEPS = 8

@dataclass
class AgentState:
    goal: str
    repo_path: str
    reports_dir: str

    observations: List[str] = field(default_factory=list)
    actions_taken: List[str] = field(default_factory=list)

    report: Dict[str, Any] = field(default_factory=dict)

    coverage_percent: float | None = None
    tests_generated: bool = False


def run_agent(repo_path: str, reports_dir: str, goal: str):
    print("🤖 SWE Agent starting")
    print(f"📁 Repo path: {repo_path}")
    print(f"🎯 Goal: {goal}")
    state = AgentState(
        goal=goal,
        repo_path=repo_path,
        reports_dir=reports_dir
    )

    for _ in range(MAX_STEPS):
        action = plan_next_action(state.goal, state.observations)
        if action in state.actions_taken:
            state.observations.append(f"Action {action} already taken, stopping")
            break

        state.actions_taken.append(action)

        if action == "stop":
            break

        execute_action(state, action)

        # hard safety stop
        if state.coverage_percent and state.coverage_percent >= 80:
            state.observations.append("Coverage goal met")
            break

    return state




