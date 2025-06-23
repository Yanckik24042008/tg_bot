import os
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gpt_interface(update: Update, context: CallbackContext):
    """Enter standard GPT chat mode."""
    context.user_data["mode"] = "gpt"
    context.user_data.pop("persona", None)

    kb = [[InlineKeyboardButton("End chat", callback_data="gpt_end")]]
    await update.message.reply_photo(
        photo=open("images/image_ai.jpg", "rb"),
        caption="Chat with GPT: send any message.",
        reply_markup=InlineKeyboardMarkup(kb),
    )

async def gpt_text_handler(update: Update, context: CallbackContext):
    """Handle text only when in GPT mode."""
    if context.user_data.get("mode") != "gpt":
        return  # not GPT mode

    user_text = update.message.text
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}],
    )
    await update.message.reply_text(resp.choices[0].message.content)

async def gpt_end_callback(update: Update, context: CallbackContext):
    """Exit GPT mode."""
    if context.user_data.get("mode") != "gpt":
        return

    context.user_data.pop("mode", None)
    await update.callback_query.edit_message_caption(
        "GPT chat ended. Use /gpt to start again."
    )
