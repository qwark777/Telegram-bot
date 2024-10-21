import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, any_state
from dotenv import load_dotenv, find_dotenv
from aiogram import F, Bot, Dispatcher, types  # внешние библиотеки
import asyncio
from aiogram.filters import StateFilter, Command
import mysql.connector
from aiogram.types import video_note
from mysql.connector import pooling, cursor
import time

from databases_functions import not_in_database, insert_full_name, insert_sex, insert_age, insert_age_find, \
    insert_sex_find, select_name, get_count_of_media, print_profile  # вспомогательные файлы
from reply import start_keyboard, del_keyboard, sex_keyboard, find_sex_keyboard

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


class USER(StatesGroup):
    registration = State()  # желание зарегестрироваться
    name = State()
    age = State()
    sex = State()
    university = State()
    image = State()
    age_find = State()
    find_sex = State()


@dp.message(StateFilter(None), F.text)
async def start(message: types.Message, state: FSMContext):
    if await not_in_database(message.from_user.id, connection_pool):
        await message.answer("Привет, я вижу, что мы не знакомы. Хочешь зарегестрироваться?",
                             reply_markup=start_keyboard)
    else:
        string = await select_name(message.from_user.id, connection_pool)
        await message.answer("Привет, {}! Хочешь продолжить наше общение?".format(string))
    await state.set_state(USER.registration)


@dp.message(USER.registration, F.text)
async def continue_registration(message: types.Message, state: FSMContext):
    if message.text == "Да ✅" or message.text.lower() == "да" or message.text == "✅" or message.text.lower() == "yes":
        await message.answer("Как тебя зовут?", reply_markup=del_keyboard)
        await state.set_state(USER.name)
    elif message.text == "Нет ❌" or message.text.lower() == "нет" or message.text == "❌" or message.text.lower() == "no":
        await message.answer("Напиши тогда, как захочешь)", reply_markup=del_keyboard)
        await state.clear()
    else:
        await message.answer("Напиши мне 'да' или 'нет' или выбери ответ на виртуальной клавиатуре",
                             reply_markup=del_keyboard)


@dp.message(USER.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer("Напиши только имя и фамилию")
    else:
        if await insert_full_name(message.from_user.id, message.text.title(), connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
            await state.clear()
        else:
            await message.answer("Ты парень или девушка?", reply_markup=sex_keyboard)
            await state.set_state(USER.sex)


@dp.message(USER.sex, F.text)
async def get_sex(message: types.Message, state: FSMContext):
    if message.text.lower() == "девушка" or message.text == "Девушка 👩‍🎓" or message.text.lower() == "girl" or message.text == "👩‍🎓":
        if await insert_sex(message.from_user.id, 0, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(USER.age)
    elif message.text.lower() == "парень" or message.text == "Парень 👨‍🎓" or message.text.lower() == "boy" or message.text == "👨‍🎓":
        if await insert_sex(message.from_user.id, 1, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(USER.find_sex)
    else:
        await message.answer("Пожалуйста напиши мне 'парень' или 'девушка' или выбери ответ на виртуальной клавиатуре")


@dp.message(USER.find_sex, F.text)
async def get_find_sex(message: types.Message, state: FSMContext):
    if message.text.lower() == "девушек" or message.text == "Девушек 👩‍🎓" or message.text.lower() == "girls" or message.text == "👩‍🎓":
        if await insert_sex_find(message.from_user.id, 0, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Сколько тебе лет?", reply_markup=del_keyboard)
            await state.set_state(USER.age)
    elif message.text.lower() == "парней" or message.text == "Парней 👨‍🎓" or message.text.lower() == "boys" or message.text == "👨‍🎓":
        if await insert_sex_find(message.from_user.id, 1, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Сколько тебе лет?", reply_markup=del_keyboard)
            await state.set_state(USER.age)
    elif message.text == "Без разницы 🤷‍♂️🤷‍♀️" or message.text.lower() == "без разницы" or message.text == "🤷‍♂️🤷‍♀️":
        if await insert_sex_find(message.from_user.id, 2, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Сколько тебе лет?", reply_markup=del_keyboard)
            await state.set_state(USER.age)
    else:
        await message.answer("Пожалуйста напиши мне 'парней', 'девушек' или 'без разницы' или выбери ответ на виртуальной клавиатуре")


@dp.message(USER.age, F.text)
async def get_age(message: types.Message, state: FSMContext):
    try:
        if await insert_age(message.from_user.id, int(message.text), connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой возраст тебя интересует? Напиши диапазон в формате YY-YY")
            await state.set_state(USER.age_find)
    except ValueError:
        await message.answer("Введи возраст числом")


@dp.message(USER.age_find, F.text)
async def get_age_find(message: types.Message, state: FSMContext):
    try:
        if int(message.text.split("-")[0]) > int(message.text.split("-")[1]):
            await message.answer("Минимальный возраст должен быть не больше максимального")
        elif int(message.text.split("-")[1]) > 255:
            await message.answer("Слишком большой максимальный возраст")
        elif await insert_age_find(message.from_user.id, int(message.text.split("-")[0]),
                                   int(message.text.split("-")[1]), connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Прикрепи свое фото")
            await state.set_state(USER.image)
    except ValueError:
        await message.answer("Введи возраст числом")
    except IndexError:
        await message.answer("Введи возраст в формате YY-YY")


@dp.message(USER.image, F.photo)
async def get_image(message: types.Message):
    number = get_count_of_media(message.from_user.id, connection_pool)
    if number == 4:
        await message.answer("К сожалению возможно только 4 медиа-файла в одной анкете. Мы взяли первые 4 файла")
    elif number == 0:
        # вставка в бд

        time.sleep(4)
        await message.answer("Отлично! Вот твоя анкета:")
        await print_profile(message.from_user.id, connection_pool)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    dbconfig = {
        "user": "root",
        "password": "12345678",
        "host": "localhost",
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=32, **dbconfig)
    asyncio.run(main())
