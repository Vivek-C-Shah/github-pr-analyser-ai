from app.ai_utils import analyze_code_with_openai

def test_analyze_code_with_openai():
    result = analyze_code_with_openai("test.py", "print('Hello, World!')")
    assert isinstance(result, dict)
    assert "issues" in result