# src/planner.py
import openai

SYSTEM_PROMPT = """
You are a software engineering agent.
Given the current goal and observations, decide the next action.

Possible actions:
- run_lint
- run_tests
- analyze_coverage
- generate_tests
- create_pr
- stop

Respond with exactly one action name.
"""


def plan_next_action(goal: str, observations: list[str]) -> str:
    prompt = f"""
Goal:
{goal}

Observations:
{chr(10).join(observations)}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message["content"].strip()
