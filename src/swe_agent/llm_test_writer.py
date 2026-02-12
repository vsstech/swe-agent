# src/llm_test_writer.py
from dataclasses import dataclass
from typing import List
from openai import OpenAI
from swe_agent.config import get_openai_key

client = OpenAI(api_key=get_openai_key())


@dataclass
class GeneratedTest:
    filename: str
    content: str


SYSTEM_PROMPT = """
You are a senior Python test engineer.
Generate pytest unit tests.
Rules:
- Use pytest
- No mocks unless required
- Clear test names
- Do not explain, only output code
"""


def generate_tests(
    source_code: str,
    suggestions: List[str],
    module_name: str,
) -> str:
    prompt = f"""
Source module:
{source_code}

Test requirements:
{chr(10).join("- " + s for s in suggestions)}

Write pytest tests for module: {module_name}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or your preferred model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
