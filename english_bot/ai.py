import json
import os

from dotenv import load_dotenv
from google.genai import types
from google.genai.client import AsyncClient, BaseApiClient

from .exceptions import AIError, ConfigError

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not GEMINI_API_KEY:
    raise ConfigError("GEMINI_API_KEY не задан в .env")

_client = AsyncClient(api_client=BaseApiClient(api_key=GEMINI_API_KEY))


SYSTEM_PROMPT = (
    "Ты — строгий, но доброжелательный репетитор английского языка. "
    "Ты помогаешь собеседникам практиковать английский.\n"
    "\n"
    "Твоя задача — анализировать сообщения и возвращать ТОЛЬКО JSON "
    "без маркдауна, без лишнего текста.\n"
    "\n"
    "Формат JSON:\n"
    "{\n"
    '  "is_russian": true/false,\n'
    '  "level": 1..6,\n'
    '  "is_correct": true/false,\n'
    '  "corrected_text": "исправленный вариант или null",\n'
    '  "explanation": "краткое объяснение на русском или null",\n'
    '  "translation": "перевод на английский как Native Speaker или null"\n'
    "}\n"
    "\n"
    "Правила:\n"
    "- is_russian=true, если сообщение написано в основном по-русски "
    "(кириллица преобладает). Тогда заполни только translation "
    "(естественный, разговорный перевод как у носителя), "
    "а level=null, is_correct=null, corrected_text=null, explanation=null.\n"
    "- Если сообщение на английском:\n"
    "  - Оцени уровень по шкале CEFR: "
    "1=ELEMENTARY, 2=LOW-INTERMEDIATE, 3=INTERMEDIATE, "
    "4=UPPER-INTERMEDIATE, 5=ADVANCED, 6=PROFICIENCY.\n"
    "  - is_correct=true, если грамматических и лексических ошибок нет.\n"
    "  - Если есть ошибки: is_correct=false, "
    "corrected_text — исправленный вариант целиком, "
    "explanation — краткое объяснение главной ошибки на русском "
    "(1-2 предложения) с подбадриванием.\n"
    "  - Если ошибок нет: corrected_text=null, explanation=null.\n"
    "- Отвечай стабильным, валидным JSON."
)


async def evaluate(text: str) -> dict:
    """Send text to Gemini and return structured analysis as a dict."""
    prompt = "Проанализируй сообщение и верни JSON:\n" + text

    chat = _client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        ),
    )
    try:
        response = await chat.send_message(prompt)
    except Exception as exc:
        raise AIError(f"Gemini API error: {exc}") from exc

    return json.loads(response.text.strip())
