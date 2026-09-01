import logging
import logging.handlers
import os

from dotenv import load_dotenv
from telegram import ReactionTypeEmoji, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from .ai import evaluate
from .exceptions import AIError, ConfigError

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
_file_handler = logging.handlers.RotatingFileHandler(
    os.path.join("logs", "bot.log"),
    maxBytes=1_000_000,
    backupCount=3,
    encoding="utf-8",
)
_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logging.getLogger().addHandler(_file_handler)
logger = logging.getLogger(__name__)

LEVEL_REACTIONS = {
    1: "🐳",
    2: "🗿",
    3: "👏",
    4: "🤩",
    5: "🔥",
    6: "💯",
}


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Process text messages: evaluate English or translate Russian."""
    message = update.effective_message
    if not message or not message.text:
        return

    try:
        result = await evaluate(message.text)
    except AIError as exc:
        logger.error("Ошибка AI: %s", exc)
        return

    if result.get("is_russian"):
        translation = result.get("translation")
        if translation:
            await message.reply_text(
                f"🇬🇧 *Как скажет носитель:*\n_{translation}_",
                parse_mode="Markdown",
            )
        return

    level = result.get("level")
    is_correct = result.get("is_correct")
    if level in LEVEL_REACTIONS:
        try:
            await message.set_reaction(
                [ReactionTypeEmoji(LEVEL_REACTIONS[level])], is_big=False
            )
        except Exception as exc:
            logger.warning("Не удалось поставить реакцию: %s", exc)

    if not is_correct:
        corrected = result.get("corrected_text")
        explanation = result.get("explanation")
        reply = f"*Исправленный вариант:*\n{corrected}"
        if explanation:
            reply += f"\n\n💡 *Почему:* {explanation}"
        await message.reply_text(reply, parse_mode="Markdown")


def main() -> None:
    """Build and run the Telegram bot polling loop."""
    if not BOT_TOKEN:
        raise ConfigError("BOT_TOKEN не задан в .env")

    app = Application.builder().token(BOT_TOKEN).build()
    handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message
    )
    app.add_handler(handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
