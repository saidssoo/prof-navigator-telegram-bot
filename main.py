import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------- ВОПРОСЫ --------

questions = [
    "1️⃣ Что тебе нравится?\n1. Логика\n2. Творчество\n3. Общение",
    "2️⃣ Как ты работаешь?\n1. Один\n2. В команде\n3. Практически",
    "3️⃣ Что важнее?\n1. Деньги\n2. Интерес\n3. Стабильность",
    "4️⃣ Любишь ли ты технологии?\n1. Да\n2. Нет",
    "5️⃣ Любишь ли ты работать с людьми?\n1. Да\n2. Нет"
]

# -------- ДАННЫЕ --------

user_step = {}
user_scores = {}

# -------- КНОПКА --------

menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать тест")]],
    resize_keyboard=True
)

# -------- START --------

@dp.message(Command("start"))
async def start(message: Message):

    user_step[message.from_user.id] = 0
    user_scores[message.from_user.id] = {
        "logic":0,
        "creative":0,
        "social":0,
        "tech":0
    }

    await message.answer(
        "Привет 👋\nНажми 'Начать тест'",
        reply_markup=menu
    )

# -------- НАЧАТЬ ТЕСТ --------

@dp.message(F.text == "Начать тест")
async def start_test(message: Message):

    await message.answer(questions[0])

# -------- ОБРАБОТКА ОТВЕТОВ --------

@dp.message()
async def answers(message: Message):

    user_id = message.from_user.id

    if user_id not in user_step:
        return

    step = user_step[user_id]
    text = message.text

    scores = user_scores[user_id]

    # ----- Баллы -----

    if step == 0:
        if text == "1":
            scores["logic"] += 2
            scores["tech"] += 1
        elif text == "2":
            scores["creative"] += 2
        elif text == "3":
            scores["social"] += 2

    elif step == 1:
        if text == "1":
            scores["logic"] += 2
        elif text == "2":
            scores["social"] += 2
        elif text == "3":
            scores["tech"] += 2

    elif step == 2:
        if text == "1":
            scores["logic"] += 2
            scores["tech"] += 1
        elif text == "2":
            scores["creative"] += 2
        elif text == "3":
            scores["social"] += 1

    elif step == 3:
        if text == "1":
            scores["tech"] += 2
        else:
            scores["creative"] += 1

    elif step == 4:
        if text == "1":
            scores["social"] += 2
        else:
            scores["logic"] += 1

    # ----- Следующий шаг -----

    step += 1
    user_step[user_id] = step

    if step < len(questions):
        await message.answer(questions[step])
    else:

        result = max(scores, key=scores.get)

        result_text = {
            "logic":"💻 IT и технические профессии",
            "creative":"🎨 Творческие профессии",
            "social":"🤝 Коммуникационные профессии",
            "tech":"⚙️ Технические профессии"
        }

        await message.answer(
            "✅ Тест завершён!\n" +
            result_text[result]
        )

# -------- ЗАПУСК --------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())