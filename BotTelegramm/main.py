
import nest_asyncio
import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
import new_quiz1
import data_bace
from quiz import quiz_data


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = '6927263595:AAEk2k7lOeE8zlLyLe6Og2RZxSTPyvk-Xis'


# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()
# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'




# Запускаем создание таблицы базы данных
#await  create_table()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz1.new_quiz(message)


def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()

@dp.callback_query(F.data.one_of(["right_answer", "wrong_answer"]))
async def handle_answer(callback: types.CallbackQuery, right_answer: bool = True):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await data_bace.get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    if right_answer:
        await callback.message.answer("Верно!")
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await data_bace.update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await new_quiz1.get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


# Запуск процесса поллинга новых апдейтов
async def main():
    #await data_bace.create_database()
    await data_bace.create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
