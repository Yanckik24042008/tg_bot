"""Модуль с командой /space для получения характеристик астрономических объектов.

Позволяет пользователю выбрать объект из списка или ввести любое имя объекта,
после чего GPT возвращает научные данные: массу, радиус, гравитацию, орбиту и интересный факт.
"""
import os
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OBJECTS = ["Sun", "Earth", "Mars", "Milky Way", "Andromeda"]

async def fetch_info(obj: str) -> str:
    """Отправляет запрос в OpenAI для получения характеристик объекта.

        Возвращает краткое описание: масса, радиус, гравитация, состав, расстояние и интересный факт.
        """
    system_msg = {
        "role": "system",
        "content": (
            "You are an expert astronomer. Provide concise data about an astronomical object: "
            "mass, radius, surface gravity, orbital period (if relevant), distance from Earth, "
            "composition, and one interesting fact."
        ),
    }
    user_msg = {"role": "user", "content": f"Give me the key characteristics of {obj}."}
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_msg, user_msg],
        temperature=0.6,
        max_tokens=400,
    )
    return resp.choices[0].message.content

async def space_fact_command(update: Update, context: CallbackContext):
    """Обрабатывает команду /space: показывает кнопки с объектами и кнопку «Finish»."""

    context.user_data["mode"] = "space"

    kb = [[InlineKeyboardButton(o, callback_data=f"space_{o}")] for o in OBJECTS]
    kb.append([InlineKeyboardButton("Finish", callback_data="space_finish")])

    await update.message.reply_text(
        "Choose an object or type any name to get its characteristics:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def space_fact_callback(update: Update, context: CallbackContext):
    """Обрабатывает нажатие кнопок после команды /space.

    Если выбрана кнопка с объектом — показывает информацию об объекте.
    Если выбрано «Finish» — возвращает главное меню.
    """
    q = update.callback_query
    await q.answer()

    if q.data == "space_finish":
        # Exit space mode and re-send main menu
        context.user_data.pop("mode", None)
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
                "or send a voice message."
            ),
        )
        return

    # Otherwise, fetch and display info
    obj = q.data.split("_", 1)[1]
    info = await fetch_info(obj)

    kb = [[InlineKeyboardButton("Finish", callback_data="space_finish")]]
    await q.edit_message_text(
        f"*{obj}*\n\n{info}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def space_text_handler(update: Update, context: CallbackContext):
    """Обрабатывает ввод вручную (текст), если пользователь в режиме /space.

    Отправляет название введённого объекта и выводит информацию о нём.
    """
    if context.user_data.get("mode") != "space":
        return

    obj = update.message.text.strip()
    info = await fetch_info(obj)

    kb = [[InlineKeyboardButton("Finish", callback_data="space_finish")]]
    await update.message.reply_text(
        f"*{obj}*\n\n{info}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )
