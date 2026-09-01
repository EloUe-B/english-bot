# English Coach Bot

> ⚠️ **Early version** of a bot for practicing English conversation.

A Telegram bot that helps you practice English right in the chat: it assesses your message level (CEFR), fixes mistakes, and translates Russian messages into natural native-speaker English.

## Features

- **CEFR level assessment** — English messages get an emoji reaction: 🐳1 ELEMENTARY, 🗿2 LOW-INTERMEDIATE, 👏3 INTERMEDIATE, 🤩4 UPPER-INTERMEDIATE, 🔥5 ADVANCED, 💯6 PROFICIENCY.
- **Error correction** — when there's a mistake, the bot replies with the corrected version and a short explanation in Russian.
- **Translation** — Russian messages are translated into natural native-speaker English.

## Requirements

- Python 3.10+
- Telegram bot token (from @BotFather)
- Gemini API key (free, at aistudio.google.com/apikey)

## Installation and Run (local)

1. Create a bot with [@BotFather](https://t.me/BotFather): `/newbot` → get the token.
2. Get a Gemini API key at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey).
3. Put the keys in `.env` (see the example in `.env.example`):

   ```
   BOT_TOKEN=your_botfather_token
   GEMINI_API_KEY=your_gemini_key
   GEMINI_MODEL=gemini-3.5-flash-lite  # optional
   ```

4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python bot.py`

## Run in Docker

```
docker compose build
docker compose up -d
```

## CI/CD

On every push to `main`, GitHub Actions runs flake8 and pytest, builds and pushes the Docker image `eloue1/english-bot` to DockerHub, then deploys to the server over SSH (`docker compose pull` + `up -d --force-recreate`) and sends a success notification to Telegram.

Required secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD` (DockerHub), `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PASSWORD`, `DEPLOY_PATH` (server), `TELEGRAM_TOKEN`, `TELEGRAM_TO` (notifications). See `.github/workflows/ci.yml` for details.

## Server Setup (one-time)

Git and source code are not needed on the server — deployment works only through the ready-made image.

1. Create the `DEPLOY_PATH` folder on the server.
2. Put `docker-compose.yml` (from this repository) and `.env` into it:
   ```
   BOT_TOKEN=your_botfather_token
   GEMINI_API_KEY=your_gemini_key
   ```
3. Run it the first time: `docker compose pull && docker compose up -d`

After that, every push to `main` pulls the fresh image and restarts the bot automatically.

## Adding the Bot to a Group

The bot replies in any chat it's added to — no separate instance is needed per group. To make it work you need a group and admin rights:

1. **Create a group**: in Telegram tap "New Message" → "New Group" → pick members → "Create".
2. **Add the bot**: open group settings → "Add Members" (or tap the group name at the top) → search for the bot by its `@username` (the name issued by @BotFather) → add it.
3. **Make the bot an admin** (required for reactions): group settings → "Administrators" → "Add Admin" → select the bot. Grant at least: **Send messages** and **Set reactions**. You can leave "Hide bot" enabled so it doesn't clutter the member list.

Done — the bot will start assessing English messages, fixing mistakes, and translating Russian ones.

## Notes

- Every call to `ai.evaluate()` creates a new chat session — the bot has no memory between messages.
- In groups the bot needs permission to set reactions (see above).
- If the bot doesn't respond, make sure it's an admin and that `.env` on the server has valid `BOT_TOKEN` and `GEMINI_API_KEY`.

## How It Works

- `bot.py` — Telegram logic (messages, reactions, replies).
- `ai.py` — Gemini call: `ai.evaluate() -> dict` (level, errors, correction, explanation, translation).

---

Russian version: [README_ru.md](README_ru.md)