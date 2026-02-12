# src/test_generation_pipeline.py
from pathlib import Path
from swe_agent.llm_test_writer import generate_tests


def generate_test_file(
    source_file: str,
    suggestions: list[str],
    tests_dir: str,
):
    source_path = Path(source_file)
    module_name = source_path.stem

    code = source_path.read_text()

    test_code = generate_tests(
        source_code=code,
        suggestions=suggestions,
        module_name=module_name,
    )

    Path(tests_dir).mkdir(exist_ok=True)

    test_file = Path(tests_dir) / f"test_{module_name}_generated.py"
    test_file.write_text(test_code)

    return str(test_file)
