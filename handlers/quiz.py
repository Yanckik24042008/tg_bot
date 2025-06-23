"""Модуль с командой /quiz для космической викторины.

Позволяет пользователю выбрать тему, проходить вопросы с вариантами ответов,
получать обратную связь и финальный результат.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

"""Вопросы"""
QUIZ_QUESTIONS = {
    "Planets": [
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Mars",
        },
        {
            "question": "What is the largest planet in our Solar System?",
            "options": ["Saturn", "Jupiter", "Neptune", "Earth"],
            "answer": "Jupiter",
        },
        {
            "question": "Which planet has the fastest orbital speed around the Sun?",
            "options": ["Mercury", "Venus", "Earth", "Mars"],
            "answer": "Mercury",
        },
        {
            "question": "Which planet is famous for its extensive ring system?",
            "options": ["Uranus", "Jupiter", "Saturn", "Neptune"],
            "answer": "Saturn",
        },
        {
            "question": "Which planet is often called Earth's 'sister planet' due to similar size and composition?",
            "options": ["Mercury", "Venus", "Mars", "Neptune"],
            "answer": "Venus",
        },
        {
            "question": "On which planet would you find the volcano Olympus Mons?",
            "options": ["Earth", "Mars", "Venus", "Mercury"],
            "answer": "Mars",
        },
        {
            "question": "Which planet has a day longer than its year?",
            "options": ["Venus", "Mercury", "Mars", "Jupiter"],
            "answer": "Venus",
        },
        {
            "question": "Which planet has the highest average density?",
            "options": ["Earth", "Mercury", "Jupiter", "Neptune"],
            "answer": "Earth",
        },
        {
            "question": "Which ice giant is farthest from the Sun?",
            "options": ["Uranus", "Neptune", "Saturn", "Jupiter"],
            "answer": "Neptune",
        },
        {
            "question": "Which planet has the strongest winds in the Solar System?",
            "options": ["Jupiter", "Saturn", "Uranus", "Neptune"],
            "answer": "Neptune",
        },
    ],
    "Stars": [
        {
            "question": "What is the nearest star to Earth after the Sun?",
            "options": ["Sirius", "Alpha Centauri A", "Proxima Centauri", "Barnard’s Star"],
            "answer": "Proxima Centauri",
        },
        {
            "question": "Our Sun is classified as which spectral type?",
            "options": ["G-type main-sequence", "K-type giant", "M-type dwarf", "F-type subgiant"],
            "answer": "G-type main-sequence",
        },
        {
            "question": "What color are the hottest stars?",
            "options": ["Red", "Yellow", "Blue", "White"],
            "answer": "Blue",
        },
        {
            "question": "Which star is known as the Dog Star?",
            "options": ["Vega", "Rigel", "Sirius", "Betelgeuse"],
            "answer": "Sirius",
        },
        {
            "question": "What is the term for a rapidly rotating neutron star emitting beams of electromagnetic radiation?",
            "options": ["Quasar", "Pulsar", "Magnetar", "Blazar"],
            "answer": "Pulsar",
        },
        {
            "question": "Which type of variable star is used as a 'standard candle' to measure cosmic distances?",
            "options": ["RR Lyrae", "Cepheid", "Mira", "T Tauri"],
            "answer": "Cepheid",
        },
        {
            "question": "Which star is the brightest in the night sky?",
            "options": ["Canopus", "Sirius", "Rigil Kentaurus", "Arcturus"],
            "answer": "Sirius",
        },
        {
            "question": "What is the approximate lifetime of a star like our Sun on the main sequence?",
            "options": ["10 million years", "100 million years", "1 billion years", "10 billion years"],
            "answer": "10 billion years",
        },
        {
            "question": "What spectral class represents the hottest stars?",
            "options": ["O", "B", "A", "F"],
            "answer": "O",
        },
        {
            "question": "What is the name of the North Star?",
            "options": ["Polaris", "Vega", "Deneb", "Altair"],
            "answer": "Polaris",
        },
    ],
    "Galaxies": [
        {
            "question": "Which galaxy is the closest large neighbor to the Milky Way?",
            "options": ["Andromeda", "Triangulum", "Whirlpool", "Sombrero"],
            "answer": "Andromeda",
        },
        {
            "question": "What type of galaxy is the Milky Way?",
            "options": ["Elliptical", "Spiral", "Irregular", "Lenticular"],
            "answer": "Spiral",
        },
        {
            "question": "Which law relates a galaxy's recessional velocity to its distance?",
            "options": ["Kepler’s Law", "Hubble’s Law", "Newton’s Law", "Ohm’s Law"],
            "answer": "Hubble’s Law",
        },
        {
            "question": "What is the name of the galaxy group that contains the Milky Way?",
            "options": ["Virgo Cluster", "Local Group", "Hercules Supercluster", "Coma Cluster"],
            "answer": "Local Group",
        },
        {
            "question": "Which galaxy is famous for its nearly edge-on appearance and prominent dust lane?",
            "options": ["Andromeda", "Triangulum", "Sombrero", "Cartwheel"],
            "answer": "Sombrero",
        },
        {
            "question": "What active and extremely luminous central region is found in some galaxies?",
            "options": ["Quasar", "Pulsar", "Nova", "Supernova"],
            "answer": "Quasar",
        },
        {
            "question": "Which is the largest known galaxy by diameter?",
            "options": ["Andromeda", "IC 1101", "Messier 87", "Whirlpool"],
            "answer": "IC 1101",
        },
        {
            "question": "Which satellite galaxy orbits the Milky Way?",
            "options": ["Large Magellanic Cloud", "Andromeda II", "M32", "Triangulum"],
            "answer": "Large Magellanic Cloud",
        },
        {
            "question": "What classification describes a galaxy without a defined shape?",
            "options": ["Spiral", "Elliptical", "Irregular", "Barred Spiral"],
            "answer": "Irregular",
        },
        {
            "question": "What term describes the vast structure of galaxy clusters to which the Milky Way belongs?",
            "options": ["Local Group", "Virgo Supercluster", "Perseus Cluster", "Great Attractor"],
            "answer": "Virgo Supercluster",
        },
    ],
}

async def start_quiz(update: Update, context: CallbackContext):
    kb = [
        [InlineKeyboardButton(topic, callback_data=f"topic_{topic}")]
        for topic in QUIZ_QUESTIONS
    ]
    await update.message.reply_text(
        "Choose an astronomy topic:", reply_markup=InlineKeyboardMarkup(kb)
    )

async def choose_topic(update: Update, context: CallbackContext):
    """Обрабатывает выбор темы и отправляет первый вопрос викторины."""
    q = update.callback_query
    await q.answer()
    topic = q.data.split("_", 1)[1]
    context.user_data["quiz_topic"] = topic
    context.user_data["quiz_index"] = 0
    context.user_data["quiz_score"] = 0

    item = QUIZ_QUESTIONS[topic][0]
    kb = [
        [InlineKeyboardButton(opt, callback_data=f"answer_0_{opt}")]
        for opt in item["options"]
    ]
    await q.edit_message_text(f"Q1: {item['question']}", reply_markup=InlineKeyboardMarkup(kb))

async def quiz_answer(update: Update, context: CallbackContext):
    """Обрабатывает ответ пользователя на текущий вопрос викторины.

        Увеличивает счёт, даёт обратную связь и переходит к следующему вопросу,
        либо завершает викторину.
        """
    q = update.callback_query
    await q.answer()
    _, idx_str, selected = q.data.split("_", 2)
    idx = int(idx_str)
    topic = context.user_data["quiz_topic"]
    item = QUIZ_QUESTIONS[topic][idx]

    if selected == item["answer"]:
        context.user_data["quiz_score"] += 1
        await q.message.reply_text("✅ Correct!")
    else:
        await q.message.reply_text(f"❌ Incorrect. Answer: {item['answer']}")

    next_idx = idx + 1
    if next_idx < len(QUIZ_QUESTIONS[topic]):
        nxt = QUIZ_QUESTIONS[topic][next_idx]
        kb = [
            [InlineKeyboardButton(opt, callback_data=f"answer_{next_idx}_{opt}")]
            for opt in nxt["options"]
        ]
        await q.message.reply_text(
            f"Q{next_idx+1}: {nxt['question']}", reply_markup=InlineKeyboardMarkup(kb)
        )
    else:
        score = context.user_data["quiz_score"]
        total = len(QUIZ_QUESTIONS[topic])
        await q.message.reply_text(f"🎉 Congratulations! Quiz finished: {score}/{total}")
        for k in ("quiz_topic", "quiz_index", "quiz_score"):
            context.user_data.pop(k, None)
