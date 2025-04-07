import pytest
from src.ai_sql import generate_sql_from_natural_language, client

# Define a fake replacement for the client's API call.
def fake_create(*args, **kwargs):
    class FakeMessage:
        def __init__(self):
            self.content = "Fake SQL Query and Explanation"
    class FakeChoice:
        def __init__(self):
            self.message = FakeMessage()
    class FakeResponse:
        def __init__(self):
            self.choices = [FakeChoice()]
    return FakeResponse()

def test_generate_sql(monkeypatch, capsys):
    # Monkey-patch the chat.completions.create method to not hit the real API.
    monkeypatch.setattr(client.chat.completions, "create", fake_create)
    generate_sql_from_natural_language("Show me all records from names table", "names table schema")
    captured = capsys.readouterr().out
    assert "Fake SQL Query and Explanation" in captured
