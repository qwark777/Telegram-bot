from collections import defaultdict
from copy import deepcopy
import aiomysql
from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from bot_functions import bot, create_inline_keyboard
from clases import User, Constants
from databases_functions import insert_sex_find, insert_age_find, insert_media, insert_type, print_registration_profile, \
    insert_description, not_in_database, select_name, insert_full_name, insert_sex, insert_age, insert_uni
from reply import start_keyboard, find_sex_keyboard, sex_keyboard, uni_keyboard, button_texts

user_reg = Router()
find_uni = defaultdict(lambda: deepcopy(button_texts))
del_messages = dict()
global connection_pool


async def create_user_router(con_pool: aiomysql.pool.Pool):
    global connection_pool
    connection_pool = con_pool


@user_reg.message(StateFilter(None), F.text)
async def start(message: types.Message, state: FSMContext):
    if await not_in_database(message.from_user.id, connection_pool):
        await message.answer("Привет, я вижу, что мы не знакомы. Хочешь зарегестрироваться?", reply_markup=start_keyboard)
        del_messages[message.from_user.id] = message.message_id
    else:
        string = await select_name(message.from_user.id, connection_pool)
        await message.answer("Привет, {}! Хочешь продолжить наше общение?".format(string))
        return
    await state.set_state(User.registration)


@user_reg.callback_query(User.registration, lambda c: c.data and c.data.startswith('btn_01_'))
async def continue_registration_cal(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 1:
        await callback_query.message.answer("Как тебя называть?")
        await state.set_state(User.name)
    elif index == 2:
        await callback_query.message.answer("Напиши тогда, как захочешь)")
        await state.clear()
    else:
        await callback_query.message.answer("Напиши мне 'да' или 'нет' или выбери ответ на виртуальной клавиатуре")
    #del
    await bot.answer_callback_query(callback_query.id)


@user_reg.message(User.name, F.text)
async def get_name_mes(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("Имя не должно превышать 50 символов")
    else:
        if await insert_full_name(message.from_user.id, message.text, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
            await state.clear()
        else:
            await message.answer("Ты парень или девушка?", reply_markup=sex_keyboard)
            await state.set_state(User.sex)


@user_reg.callback_query(User.sex, lambda c: c.data and c.data.startswith('btn_02_'))
async def get_sex_cal(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 2:
        if await insert_sex(callback_query.message.from_user.id, Constants.girl, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    elif index == 1:
        if await insert_sex(callback_query.message.from_user.id, Constants.guy, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    elif index == 99:
        await callback_query.message.answer("Как тебя называть?")
        await state.set_state(User.name)
    else:
        await callback_query.message.answer("Пожалуйста напиши мне 'парень' или 'девушка' или выбери ответ на виртуальной клавиатуре")

    await bot.answer_callback_query(callback_query.id)


@user_reg.callback_query(User.find_sex, lambda c: c.data and c.data.startswith('btn_03_'))
async def get_find_sex_cal(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 2:
        if await insert_sex_find(callback_query.message.from_user.id, Constants.girl, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.age)
    elif index == 1:
        if await insert_sex_find(callback_query.message.from_user.id, Constants.guy, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.age)
    elif index == 3:
        if await insert_sex_find(callback_query.message.from_user.id, Constants.someone, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.age)
    elif index == 99:
        await callback_query.message.answer("Ты парень или девушка?", reply_markup=sex_keyboard)
        await state.set_state(User.sex)
    else:
        await callback_query.message.answer("Пожалуйста напиши мне 'парней', 'девушек' или 'без разницы' или выбери ответ на виртуальной клавиатуре")

    await bot.answer_callback_query(callback_query.id)


@user_reg.message(User.age, F.text)
async def get_age(message: types.Message, state: FSMContext):
    try:
        if int(message.text) < 14:
            await message.answer("Сожалею, но тебе должно быть не меньше 14")
        elif int(message.text) > 255:
            await message.answer("Слишком большой возраст")
        elif await insert_age(message.from_user.id, int(message.text), connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой возраст тебя интересует? Напиши диапазон в формате YY-YY")
            await state.set_state(User.age_find)
    except ValueError:
        await message.answer("Введи возраст числом")


@user_reg.message(User.age_find, F.text)
async def get_age_find(message: types.Message, state: FSMContext):
    try:
        if int(message.text.split("-")[0]) > int(message.text.split("-")[1]):
            await message.answer("Минимальный возраст должен быть не больше максимального")
        elif int(message.text.split("-")[1]) > 255:
            await message.answer("Слишком большой возраст")
        elif await insert_age_find(message.from_user.id, int(message.text.split("-")[0]),
                                   int(message.text.split("-")[1]), connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Прикрепи свое фото. Максимум 4")
            await state.set_state(User.university)
    except ValueError:
        await message.answer("Введи возраст числом")
    except IndexError:
        await message.answer("Введи возраст в формате YY-YY")


@user_reg.callback_query(User.university, lambda c: c.data and c.data.startswith('btn_03_'))
async def get_uni(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 1:
        if await insert_uni(callback_query.message.from_user.id, Constants.MSU, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif index == 2:
        if await insert_uni(callback_query.message.from_user.id, Constants.HSE, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif index == 3:
        if await insert_uni(callback_query.message.from_user.id, Constants.RANEPA, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif index == 4:
        if await insert_uni(callback_query.message.from_user.id, Constants.BMSTU, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif index == 5:
        if await insert_uni(callback_query.message.from_user.id, Constants.MIREA, connection_pool):
            await callback_query.message.answer("В боте произошла ошибка, напиши позже")
        else:
            await callback_query.message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif index == 99:
        await callback_query.message.answer("Какой возраст тебя интересует? Напиши диапазон в формате YY-YY")
        await state.set_state(User.age_find)

    else:
        await callback_query.message.answer("Выбери ответ на виртуальной клавиатуре")

    await bot.answer_callback_query(callback_query.id)


@user_reg.callback_query(User.find_university, lambda c: c.data and c.data.startswith('btn'))
async def keyboard_handler(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index  == 100:
        await callback_query.message.answer("Отправь свое фото или видео")
        await state.set_state(User.image)
    elif index  == 99:
        pass
    else:
        if find_uni[callback_query.from_user.id][index-1][-1] == '❌':
            char = '✅'
        else:
            char = '❌'
        find_uni[callback_query.from_user.id][index-1] = f"{find_uni[callback_query.from_user.id][index-1][:-1]}{char}"
        try:
            await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=await create_inline_keyboard(find_uni[callback_query.from_user.id]))
        except Exception as e:
            print(e)

    await bot.answer_callback_query(callback_query.id)


@user_reg.message(User.image, F.content_type.in_([F.PHOTO, F.VIDEO]))
async def get_album(message: types.Message, album: list[types.Message] = None, state: FSMContext = 0):
    if not album:
        return
    counter = 1
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            if await insert_media(message.from_user.id, file_id, counter, connection_pool):
                await message.answer("В боте произошла ошибка, напиши позже")
            if await insert_type(message.from_user.id, Constants.photo, counter, connection_pool):
                await message.answer("В боте произошла ошибка, напиши позже")
        elif msg.video:
            file_id = msg.video.file_id
            if await insert_media(message.from_user.id, file_id, counter, connection_pool):
                await message.answer("В боте произошла ошибка, напиши позже")
            if await insert_type(message.from_user.id, Constants.video, counter, connection_pool):
                await message.answer("В боте произошла ошибка, напиши позже")
        counter += 1
    await message.answer("Расскажи немного о себе. Если не хочешь, просто отправь '-'")
    await state.set_state(User.description)


@user_reg.message(User.image)
async def get_any(message: types.Message, state: FSMContext):
    await message.answer("Отправь пожалуйста фото или видео")


@user_reg.message(User.description, F.text)
async def get_desc(message: types.Message, state: FSMContext):
    if len(message.text) > 200:
        await message.answer("Должно быть не больше 200 символов")
    elif message.text == "-":
        if await insert_description(message.from_user.id, "", connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await print_registration_profile(message.from_user.id, connection_pool, bot)
            await state.set_state(User.wait)
    else:
        if await insert_description(message.from_user.id, message.text, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await print_registration_profile(message.from_user.id, connection_pool, bot)
            await state.set_state(User.wait)


@user_reg.message(User.wait, F.text)
async def get_answer(message: types.Message, state: FSMContext):
    await message.answer("Отправь пожалуйста фото или видео")


