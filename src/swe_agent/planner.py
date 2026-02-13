# src/planner.py
from openai import OpenAI
from swe_agent.config import get_openai_key

client = OpenAI(api_key=get_openai_key())

SYSTEM_PROMPT = """
You are a software engineering agent.
Given the current goal and observations, decide the next action.

Allowed actions:
- run_lint
- run_tests
- analyze_coverage
- generate_tests
- dependency_analysis
- write_report
- create_pr
- stop

Rules:
- If coverage meets goal, stop or create_pr
- Do NOT repeat the same action unnecessarily
- Prefer cheapest actions first
- Respond with ONLY the action name
"""


def plan_next_action(goal: str, observations: list[str]) -> str:
    prompt = f"""
Goal:
{goal}

Observations:
{chr(10).join(observations)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
