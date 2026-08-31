import json
from unittest.mock import MagicMock, patch

with patch("os.getenv", return_value="fake-key"), \
     patch("google.genai.Client"):
    import ai


def test_evaluate_russian():
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "is_russian": True,
        "level": None,
        "is_correct": None,
        "corrected_text": None,
        "explanation": None,
        "translation": "How are you today?",
    })

    mock_chat = MagicMock()
    mock_chat.send_message.return_value = mock_response

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = ai.evaluate("Привет, как дела?")

    assert result["is_russian"] is True
    assert result["translation"] == "How are you today?"
    assert result["level"] is None


def test_evaluate_english_correct():
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "is_russian": False,
        "level": 4,
        "is_correct": True,
        "corrected_text": None,
        "explanation": None,
        "translation": None,
    })

    mock_chat = MagicMock()
    mock_chat.send_message.return_value = mock_response

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = ai.evaluate("I have been studying English for years.")

    assert result["is_russian"] is False
    assert result["level"] == 4
    assert result["is_correct"] is True


def test_evaluate_english_incorrect():
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "is_russian": False,
        "level": 2,
        "is_correct": False,
        "corrected_text": "I have a cat.",
        "explanation": "Use 'a' instead of 'one' with "
                       "singular countable nouns.",
        "translation": None,
    })

    mock_chat = MagicMock()
    mock_chat.send_message.return_value = mock_response

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = ai.evaluate("I have one cat.")

    assert result["is_correct"] is False
    assert result["corrected_text"] == "I have a cat."


def test_evaluate_invalid_json():
    mock_response = MagicMock()
    mock_response.text = "not json at all"

    mock_chat = MagicMock()
    mock_chat.send_message.return_value = mock_response

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        try:
            ai.evaluate("test")
            assert False, "Should raise"
        except (json.JSONDecodeError, ValueError):
            pass
