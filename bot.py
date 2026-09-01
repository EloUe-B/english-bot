import logging
import os

from dotenv import load_dotenv
from telegram import ReactionTypeEmoji, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from ai import evaluate

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
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
    message = update.effective_message
    if not message or not message.text:
        return

    try:
        result = evaluate(message.text)
    except Exception as exc:
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
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в .env")

    app = Application.builder().token(BOT_TOKEN).build()
    handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message
    )
    app.add_handler(handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
