from src.llm_test_writer import generate_tests


def test_generate_tests(monkeypatch):
    def fake_create(*args, **kwargs):
        class Fake:
            choices = [
                type("obj", (), {
                    "message": {"content": "def test_example(): assert True"}
                })
            ]
        return Fake()

    import openai
    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)

    result = generate_tests(
        source_code="def add(a,b): return a+b",
        suggestions=["Add test for valid input"],
        module_name="calc",
    )

    assert "test_example" in result
