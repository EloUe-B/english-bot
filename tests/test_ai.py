import json
from unittest.mock import AsyncMock, MagicMock, patch

with patch("os.getenv", return_value="fake-key"):
    import english_bot.ai as ai


async def _mock_chat(response_text: str) -> MagicMock:
    mock_chat = MagicMock()
    mock_chat.send_message = AsyncMock(
        return_value=MagicMock(text=response_text)
    )
    return mock_chat


async def test_evaluate_russian():
    mock_chat = await _mock_chat(json.dumps({
        "is_russian": True,
        "level": None,
        "is_correct": None,
        "corrected_text": None,
        "explanation": None,
        "translation": "How are you today?",
    }))

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = await ai.evaluate("Привет, как дела?")

    assert result["is_russian"] is True
    assert result["translation"] == "How are you today?"
    assert result["level"] is None


async def test_evaluate_english_correct():
    mock_chat = await _mock_chat(json.dumps({
        "is_russian": False,
        "level": 4,
        "is_correct": True,
        "corrected_text": None,
        "explanation": None,
        "translation": None,
    }))

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = await ai.evaluate("I have been studying English for years.")

    assert result["is_russian"] is False
    assert result["level"] == 4
    assert result["is_correct"] is True


async def test_evaluate_english_incorrect():
    mock_chat = await _mock_chat(json.dumps({
        "is_russian": False,
        "level": 2,
        "is_correct": False,
        "corrected_text": "I have a cat.",
        "explanation": "Use 'a' instead of 'one' with "
                       "singular countable nouns.",
        "translation": None,
    }))

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        result = await ai.evaluate("I have one cat.")

    assert result["is_correct"] is False
    assert result["corrected_text"] == "I have a cat."


async def test_evaluate_invalid_json():
    mock_chat = await _mock_chat("not json at all")

    with patch.object(ai._client.chats, "create", return_value=mock_chat):
        try:
            await ai.evaluate("test")
            assert False, "Should raise"
        except (json.JSONDecodeError, ValueError):
            pass
