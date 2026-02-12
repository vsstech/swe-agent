# swe_agent/config.py
import os
from dotenv import load_dotenv
load_dotenv()
def get_openai_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. "
            "Set it as a GitHub Actions secret or environment variable."
        )
    return key