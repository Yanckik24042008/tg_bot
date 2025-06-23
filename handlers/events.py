"""Модуль с астрономическими событиями и датами.

Позволяет пользователю ввести дату и местоположение,
после чего получает список астрономических явлений с помощью OpenAI.
"""
import os
from datetime import datetime
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
"""Обрабатывает команду /events. Запрашивает у пользователя дату."""
async def events_command(update: Update, context: CallbackContext):
    context.user_data["events_step"] = "date"
    await update.message.reply_text(
        "🗓 Please enter a date in YYYY-MM-DD (e.g. 2025-06-17) or type 'today':"
    )


async def events_text_handler(update: Update, context: CallbackContext):
    """Обрабатывает текстовые ответы на стадии ввода даты и местоположения.

        В зависимости от стадии диалога (дата → местоположение),
        обращается к OpenAI и получает список астрономических событий.
        """
    step = context.user_data.get("events_step")
    if step == "date":
        text = update.message.text.strip()
        if text.lower() == "today":
            date_str = datetime.utcnow().date().isoformat()
        else:
            try:
                datetime.strptime(text, "%Y-%m-%d")
                date_str = text
            except ValueError:
                return await update.message.reply_text(
                    "❗ Invalid date. Use YYYY-MM-DD or 'today'."
                )
        context.user_data["events_date"] = date_str
        context.user_data["events_step"] = "location"
        return await update.message.reply_text(
            f"📍 Date set to *{date_str}*.\n"
            "Now enter your location (e.g. `Belgrade, Serbia`):",
            parse_mode="Markdown",
        )

    if step == "location":
        date_str = context.user_data.pop("events_date", None)
        loc = update.message.text.strip()
        context.user_data.pop("events_step", None)

        system_msg = {
            "role": "system",
            "content": (
                "You are an expert astronomer. Given a date and a location, "
                "list all astronomical events visible there (eclipses, meteor showers, "
                "moon phases, planet positions, ISS passes, etc.). For each event include "
                "local time, how to observe it, and one fun fact."
            ),
        }
        user_msg = {
            "role": "user",
            "content": f"Date: {date_str}\nLocation: {loc}\n\nList all events in bullet-list format.",
        }
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_msg, user_msg],
            temperature=0.7,
            max_tokens=600,
        )
        events_text = resp.choices[0].message.content

        kb = [[InlineKeyboardButton("Finish", callback_data="events_finish")]]
        return await update.message.reply_text(
            events_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
        )


    return
"""Обрабатывает нажатие кнопки 'Finish' и возвращает пользователя в главное меню."""
async def events_finish_callback(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    context.user_data.pop("events_step", None)
    context.user_data.pop("events_date", None)

    # возвращаем в главное меню:
    await context.bot.send_photo(
        chat_id=q.message.chat.id,
        photo=open("images/image_ai.jpg", "rb"),
        caption=(
            "Welcome! 🤖\n\n"
            "/random  — image facts\n"
            "/quiz    — astronomy quiz\n"
            "/gpt     — chat with GPT\n"
            "/talk    — historical figures\n"
            "/space   — space object info\n"
            "/events  — custom astro events\n"
            "/resume  — upload your resume\n"

        ),
    )
