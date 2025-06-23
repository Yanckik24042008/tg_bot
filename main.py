import os
import asyncio
import logging
from dotenv import load_dotenv

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)


load_dotenv()
TG_BOT_TOKEN   = os.getenv("TG_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not TG_BOT_TOKEN or not OPENAI_API_KEY:
    print("❌ TG_BOT_TOKEN or OPENAI_API_KEY is missing")
    exit(1)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


from handlers.random        import random_fact_command, random_fact_callback
from handlers.quiz          import start_quiz, choose_topic, quiz_answer
from handlers.events        import events_command, events_text_handler, events_finish_callback
from handlers.spaceinfo     import space_fact_command, space_fact_callback, space_text_handler
from handlers.gpt_interface import gpt_interface, gpt_text_handler, gpt_end_callback
from handlers.talk          import talk_command, talk_choice_callback, talk_text_handler, talk_end_callback


async def start(update: Update, context):
    await update.message.reply_photo(
        photo=open("images/Изображение 1.jpg", "rb"),
        caption=(
            "Welcome! 🤖\n\n"
            "/random  — image facts\n"
            "/quiz    — astronomy quiz\n"
            "/gpt     — chat with GPT\n"
            "/talk    — historical figures\n"
            "/space   — space object info\n"
            "/events  — custom astro events\n"
            "or send a voice message."
        ),
    )


def main():
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    # ── Handlers ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start))

    # /random
    app.add_handler(CommandHandler("random", random_fact_command))
    app.add_handler(CallbackQueryHandler(random_fact_callback, pattern="^(another_fact|finish)$"))

    # /quiz
    app.add_handler(CommandHandler("quiz", start_quiz))
    app.add_handler(CallbackQueryHandler(choose_topic, pattern="^topic_"))
    app.add_handler(CallbackQueryHandler(quiz_answer, pattern="^answer_"))

    # /events
    app.add_handler(CommandHandler("events", events_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, events_text_handler))
    app.add_handler(CallbackQueryHandler(events_finish_callback, pattern="^events_finish$"))

    # /space
    app.add_handler(CommandHandler("space", space_fact_command))
    app.add_handler(CallbackQueryHandler(space_fact_callback, pattern="^space_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, space_text_handler))

    # /gpt
    app.add_handler(CommandHandler("gpt", gpt_interface), group=1)
    app.add_handler(CallbackQueryHandler(gpt_end_callback, pattern="^gpt_end$"), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_text_handler), group=1)

    # /talk
    app.add_handler(CommandHandler("talk", talk_command), group=2)
    app.add_handler(CallbackQueryHandler(talk_choice_callback, pattern="^persona_"), group=2)
    app.add_handler(CallbackQueryHandler(talk_end_callback, pattern="^end_talk$"), group=2)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk_text_handler), group=2)


    async def run():
        await app.bot.delete_webhook(drop_pending_updates=True)
        print("✅ Bot is running via polling!")
        await app.run_polling()

    asyncio.run(run())


if __name__ == "__main__":
    main()
