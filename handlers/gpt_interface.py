"""Модуль с командой /gpt для общения с ИИ через OpenAI.

Позволяет пользователю начать обычный чат с GPT, отправлять сообщения
и завершать диалог по кнопке.
"""
import os
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gpt_interface(update: Update, context: CallbackContext):
    """Обрабатывает команду /gpt и запускает режим чата с ИИ.

    Устанавливает флаг 'gpt' в user_data и показывает кнопку завершения чата.
    """
    context.user_data["mode"] = "gpt"
    context.user_data.pop("persona", None)

    kb = [[InlineKeyboardButton("End chat", callback_data="gpt_end")]]
    await update.message.reply_photo(
        photo=open("images/image_ai.jpg", "rb"),
        caption="Chat with GPT: send any message.",
        reply_markup=InlineKeyboardMarkup(kb),
    )

"""Обрабатывает текстовые сообщения в режиме GPT.

    Если пользователь находится в режиме GPT, передаёт сообщение в OpenAI
    и отправляет ответ от модели в чат.
    """
async def gpt_text_handler(update: Update, context: CallbackContext):

    if context.user_data.get("mode") != "gpt":
        return  # not GPT mode

    user_text = update.message.text
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}],
    )
    await update.message.reply_text(resp.choices[0].message.content)

"""Завершает режим GPT по нажатию кнопки 'End chat'.

    Удаляет флаг режима и изменяет подпись к сообщению.
    """
async def gpt_end_callback(update: Update, context: CallbackContext):

    if context.user_data.get("mode") != "gpt":
        return

    context.user_data.pop("mode", None)
    await update.callback_query.edit_message_caption(
        "GPT chat ended. Use /gpt to start again."
    )
