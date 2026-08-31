# English Coach Bot

> ⚠️ **Ранняя версия** бота для тренировки общения на английском.

Telegram-бот, который помогает практиковать английский прямо в чате: оценивает уровень сообщений, исправляет ошибки и переводит русские сообщения на английский как носитель языка.

## Возможности

- **Оценка уровня (CEFR)** — на английское сообщение ставится реакция-эмодзи уровня: 🐳1 ELEMENTARY, 🗿2 LOW-INTERMEDIATE, 👏3 INTERMEDIATE, 🤩4 UPPER-INTERMEDIATE, 🔥5 ADVANCED, 💯6 PROFICIENCY.
- **Исправление ошибок** — при ошибке бот отвечает исправленным вариантом и кратким объяснением на русском.
- **Перевод** — русское сообщение переводится на английский как Native Speaker.

## Требования

- Python 3.10+
- Telegram-бот-токен (от @BotFather)
- API-ключ Gemini (бесплатный, с aistudio.google.com/apikey)

## Установка и запуск (локально)

1. Создай бота у [@BotFather](https://t.me/BotFather): `/newbot` → получишь токен.
2. Получи ключ Gemini на [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey).
3. Впиши ключи в `.env` (см. `пример в .env.example`):

   ```
   BOT_TOKEN=токен_от_botfather
   CHAT_TOKEN=id_чата        # необязательно
   GEMINI_API_KEY=ключ_gemini
   GEMINI_MODEL=gemini-3.5-flash-lite  # необязательно
   ```

4. Установи зависимости: `pip install -r requirements.txt`
5. Запусти: `python bot.py`

## Запуск в Docker

```
docker compose build
docker compose up -d
```

## CI/CD

При пуше в `main` GitHub Actions прогоняет flake8 и pytest, затем деплоит на сервер по SSH (нужны секреты `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`, `DEPLOY_PATH`). Подробнее — `.github/workflows/ci.yml`.

## Примечания

- `CHAT_TOKEN` — необязательный фильтр: если задан, бот обрабатывает сообщения только из этого чата.
- В группе боту нужно право ставить реакции (добавляй как администратора).

## Как это работает

- `bot.py` — Telegram-логика (сообщения, реакции, ответы).
- `ai.py` — вызов Gemini: `ai.evaluate() -> dict` (уровень, ошибки, исправление, объяснение, перевод).
