

import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext


FACTS = [
    "There are more stars in the observable universe than grains of sand on all the beaches on Earth.",
    "The Sun contains 99.86% of the mass of the entire Solar System.",
    "A day on Venus (243 Earth days) is longer than its year (225 Earth days).",
    "Jupiter’s Great Red Spot is a storm twice the size of Earth—and it’s been raging for over 300 years.",
    "Saturn could float in water because its average density is less than water’s.",
    "Neutron stars can spin up to 600 times per second.",
    "Mercury experiences temperatures from –173 °C at night to 427 °C during the day.",
    "A teaspoon of neutron star material would weigh about 6 billion tons on Earth.",
    "The Milky Way galaxy is on a collision course with the Andromeda galaxy in about 4 billion years.",
    "Black holes warp spacetime so much that not even light can escape.",
    "Earth’s magnetic field flips polarity every few hundred thousand years.",
    "Mars hosts the largest volcano in the Solar System, Olympus Mons, which is about 22 km high.",
    "Neptune orbits the Sun once every 165 Earth years.",
    "A light-year is approximately 9.46 trillion kilometers.",
    "The International Space Station travels around Earth every 90 minutes.",
    "Dark matter makes up about 27% of the universe’s mass–energy content.",
    "Dark energy accounts for roughly 68% of the universe and drives its accelerated expansion.",
    "On Saturn, scientists suspect it literally rains diamonds deep in the atmosphere.",
    "Voyager 1, launched in 1977, is the farthest human-made object from Earth.",
    "The Hubble Space Telescope orbits at about 540 km above Earth.",
    "The speed of light in vacuum is about 299,792 kilometers per second.",
    "Our Sun will exhaust its nuclear fuel in about 5 billion years and become a red giant.",
    "Pluto, once the ninth planet, was reclassified as a dwarf planet in 2006.",
    "The largest asteroid in our Solar System is Ceres, about 940 km in diameter.",
    "A cosmic year (time Sun takes to orbit the Milky Way) is about 225–250 million Earth years.",
    "The first human-made object to reach space was V-2 rocket No. 6 in 1944.",
]

def get_random_fact() -> str:
    """Возвращает случайный факт."""
    return random.choice(FACTS)

async def random_fact_command(update: Update, context: CallbackContext):
    """Обработчик команды /random — сразу отправляет факт и кнопки."""
    fact = get_random_fact()
    keyboard = [
        [InlineKeyboardButton("Another fact", callback_data="another_fact")],
        [InlineKeyboardButton("Finish",       callback_data="finish")],
    ]
    await update.message.reply_text(
        fact,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def random_fact_callback(update: Update, context: CallbackContext):
    """Обработчик кнопок «Another fact» и «Finish»."""
    q = update.callback_query
    await q.answer()

    if q.data == "another_fact":
        fact = get_random_fact()
        keyboard = [
            [InlineKeyboardButton("Another fact", callback_data="another_fact")],
            [InlineKeyboardButton("Finish",       callback_data="finish")],
        ]
        await q.edit_message_text(
            fact,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:

        await q.edit_message_text("Thanks for exploring these facts! 🌌")
