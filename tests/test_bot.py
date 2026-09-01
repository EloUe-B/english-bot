from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import bot


def _make_update(text=None, chat_id="123"):
    msg = MagicMock()
    msg.text = text
    msg.reply_text = AsyncMock()
    msg.set_reaction = AsyncMock()

    chat = MagicMock()
    chat.id = chat_id

    update = MagicMock()
    update.effective_message = msg
    update.effective_chat = chat
    return update, msg


@pytest.mark.asyncio
@patch.object(bot, "evaluate")
async def test_handle_message_non_text(mock_eval):
    update = MagicMock()
    update.effective_message = None
    await bot.handle_message(update, None)
    mock_eval.assert_not_called()


@pytest.mark.asyncio
@patch.object(bot, "evaluate", return_value={
    "is_russian": True, "level": None, "is_correct": None,
    "corrected_text": None, "explanation": None,
    "translation": "How are you?",
})
async def test_handle_message_russian(mock_eval):
    update, msg = _make_update("Привет!")
    await bot.handle_message(update, None)
    msg.reply_text.assert_awaited_once()
    assert "How are you?" in msg.reply_text.call_args[0][0]


@pytest.mark.asyncio
@patch.object(bot, "evaluate", return_value={
    "is_russian": False, "level": 4, "is_correct": True,
    "corrected_text": None, "explanation": None, "translation": None,
})
async def test_handle_message_english_correct(mock_eval):
    update, msg = _make_update("Hello!")
    await bot.handle_message(update, None)
    msg.set_reaction.assert_awaited_once()
    msg.reply_text.assert_not_awaited()


@pytest.mark.asyncio
@patch.object(bot, "evaluate", return_value={
    "is_russian": False, "level": 2, "is_correct": False,
    "corrected_text": "I have a cat.",
    "explanation": "Use 'a' instead of 'an'.",
    "translation": None,
})
async def test_handle_message_english_incorrect(mock_eval):
    update, msg = _make_update("I have an cat.")
    await bot.handle_message(update, None)
    msg.set_reaction.assert_awaited_once()
    msg.reply_text.assert_awaited_once()
    assert "I have a cat." in msg.reply_text.call_args[0][0]


@pytest.mark.asyncio
@patch.object(bot, "evaluate", side_effect=RuntimeError("API error"))
async def test_handle_message_ai_error(mock_eval):
    update, msg = _make_update("Hello!")
    await bot.handle_message(update, None)
    msg.reply_text.assert_not_awaited()


def test_level_reactions_keys():
    assert set(bot.LEVEL_REACTIONS.keys()) == {1, 2, 3, 4, 5, 6}
    for emoji in bot.LEVEL_REACTIONS.values():
        assert isinstance(emoji, str)
        assert len(emoji) > 0
