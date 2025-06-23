import os
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


PERSONAS = {
    "Einstein": {
        "role": "system",
        "content": (
            "You are Albert Einstein. Always speak in first person, mention "
            "March 14, 1879, E=mc², Nobel Prize 1921, personal anecdotes. "
            "You are not an AI—imagine you are the real Einstein and answer like him."
        ),
    },
    "Hawking": {
        "role": "system",
        "content": (
            "You are Stephen Hawking. Speak in first person about black holes, "
            "cosmology, your life at Cambridge. You are not an AI—imagine you are "
            "the real Hawking and answer like him."
        ),
    },
    "Perelman": {
        "role": "system",
        "content": (
            "You are Grigori Perelman. Speak in first person about the Poincaré "
            "conjecture and your personal philosophy. You are not an AI—imagine "
            "you are the real Perelman and answer like him."
        ),
    },
    "Hubble": {
        "role": "system",
        "content": (
            "You are Edwin Hubble. Speak in first person about discovering the "
            "expansion of the universe at Mt Wilson Observatory. You are not an AI—"
            "imagine you are the real Hubble and answer like him."
        ),
    },
    "Tesla": {
        "role": "system",
        "content": (
            "You are Nikola Tesla. Speak in first person about AC current, "
            "Wardenclyffe Tower, and your visions for the future. You are not an AI—"
            "imagine you are the real Tesla and answer like him."
        ),
    },
}

async def talk_command(update: Update, context: CallbackContext):
    """Enter persona mode."""
    context.user_data["mode"] = "talk"
    context.user_data.pop("persona", None)

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"persona_{name}")]
        for name in PERSONAS
    ]
    await update.message.reply_text(
        "Choose a persona to speak with:", reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def talk_choice_callback(update: Update, context: CallbackContext):
    """Persona selected → save it and send photo."""
    if context.user_data.get("mode") != "talk":
        return

    q = update.callback_query
    await q.answer()
    persona = q.data.split("_", 1)[1]
    context.user_data["persona"] = persona

    await q.edit_message_text(
        f"You chose *{persona}*. Ask your question now!", parse_mode="Markdown"
    )

    # Send persona photo Einstein.jpg, Hawking.jpg, etc.
    photo_path = os.path.join("images", f"{persona}.jpg")
    if os.path.exists(photo_path):
        await context.bot.send_photo(
            chat_id=q.message.chat_id,
            photo=open(photo_path, "rb"),
            caption=f"📸 *{persona}*", parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text=f"⚠️ Photo not found: `{photo_path}`", parse_mode="Markdown"
        )

async def talk_text_handler(update: Update, context: CallbackContext):
    """Handle text only when in talk mode & persona chosen."""
    if context.user_data.get("mode") != "talk":
        return  # not persona mode

    persona = context.user_data.get("persona")
    if not persona:
        # persona not chosen yet — do nothing
        return

    system_msg = PERSONAS[persona]
    user_msg = {"role": "user", "content": update.message.text}

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_msg, user_msg],
        temperature=0.8,
    )
    await update.message.reply_text(resp.choices[0].message.content)

async def talk_end_callback(update: Update, context: CallbackContext):
    """Exit persona mode."""
    if context.user_data.get("mode") != "talk":
        return

    context.user_data.pop("persona", None)
    context.user_data.pop("mode", None)
    await update.callback_query.edit_message_text(
        "Conversation ended. Use /talk to start again."
    )
