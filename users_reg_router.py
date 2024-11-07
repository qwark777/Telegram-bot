from collections import defaultdict
from copy import deepcopy

from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from pyexpat.errors import messages

from bot_functions import get_connection_pool, bot, create_inline_keyboard
from clases import User, Constants
from databases_functions import insert_sex_find, insert_age_find, insert_media, insert_type, print_registration_profile, \
    insert_description, not_in_database, select_name, insert_full_name, insert_sex, insert_age, insert_uni
from reply import del_keyboard, start_keyboard, find_sex_keyboard, sex_keyboard, uni_keyboard, button_texts, back_keyboard


user_reg = Router()
find_uni = defaultdict(lambda: deepcopy(button_texts))


@user_reg.callback_query(User.find_university, lambda c: c.data and c.data.startswith('btn'))
async def keyboard_handler(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index  == 100:
        await callback_query.message.answer("Сколько тебе лет?")
        await state.set_state(User.age)
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


@user_reg.callback_query(lambda c: c.data and c.data == 'btn_99')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == User.age:
        await callback_query.message.answer("Как тебя называть?", reply_markup=back_keyboard)
        await state.set_state(User.name)
    elif current_state == User.name:
        await callback_query.message.reply("Пожалуйста, введите свое имя.")
    else:
        await callback_query.message.reply("Состояние не распознано или его нет.")

    await bot.answer_callback_query(callback_query.id)


@user_reg.callback_query(lambda c: c.data and c.data.startswith('btn'))
async def passsss(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)


@user_reg.message(Command("profile"), F.text)
async def print_profile(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
    await print_registration_profile(message.from_user.id, connection_pool, bot)


@user_reg.message(StateFilter(None), F.text)
async def start(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
    if await not_in_database(message.from_user.id, connection_pool):
        await message.answer("Привет, я вижу, что мы не знакомы. Хочешь зарегестрироваться?",
                             reply_markup=start_keyboard)
    else:
        string = await select_name(message.from_user.id, connection_pool)
        await message.answer("Привет, {}! Хочешь продолжить наше общение?".format(string))
    await state.set_state(User.registration)


@user_reg.message(User.registration, F.text)
async def continue_registration(message: types.Message, state: FSMContext):

    if message.text == "Да ✅" or message.text.lower() == "да" or message.text == "✅" or message.text.lower() == "yes":
        await message.answer("Как тебя называть?", reply_markup=del_keyboard)
        await message.answer(" ", reply_markup=back_keyboard)
        await state.set_state(User.name)
    elif message.text == "Нет ❌" or message.text.lower() == "нет" or message.text == "❌" or message.text.lower() == "no":
        await message.answer("Напиши тогда, как захочешь)", reply_markup=del_keyboard)
        await state.clear()
    else:
        await message.answer("Напиши мне 'да' или 'нет' или выбери ответ на виртуальной клавиатуре",
                             reply_markup=del_keyboard)


@user_reg.message(User.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
    if len(message.text) > 50:
        await message.answer("Имя не должно превышать 50 символов")
    else:
        if await insert_full_name(message.from_user.id, message.text, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
            await state.clear()
        else:
            await message.answer("Ты парень или девушка?", reply_markup=sex_keyboard)
            await state.set_state(User.sex)


@user_reg.message(User.sex, F.text)
async def get_sex(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
    if message.text.lower() == "девушка" or message.text == "Девушка 👩‍🎓" or message.text.lower() == "girl" or message.text == "👩‍🎓":
        if await insert_sex(message.from_user.id, Constants.girl, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    elif message.text.lower() == "парень" or message.text == "Парень 👨‍🎓" or message.text.lower() == "boy" or message.text == "👨‍🎓":
        if await insert_sex(message.from_user.id, Constants.guy, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    else:
        await message.answer("Пожалуйста напиши мне 'парень' или 'девушка' или выбери ответ на виртуальной клавиатуре")


@user_reg.message(User.find_sex, F.text)
async def get_find_sex(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
    if message.text.lower() == "девушек" or message.text == "Девушек 👩‍🎓" or message.text.lower() == "girls" or message.text == "👩‍🎓":
        if await insert_sex_find(message.from_user.id, Constants.girl, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    elif message.text.lower() == "парней" or message.text == "Парней 👨‍🎓" or message.text.lower() == "boys" or message.text == "👨‍🎓":
        if await insert_sex_find(message.from_user.id, Constants.guy, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    elif message.text == "Без разницы 🤷‍♂️🤷‍♀️" or message.text.lower() == "без разницы" or message.text == "🤷‍♂️🤷‍♀️":
        if await insert_sex_find(message.from_user.id, Constants.someone, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже", reply_markup=del_keyboard)
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    else:
        await message.answer("Пожалуйста напиши мне 'парней', 'девушек' или 'без разницы' или выбери ответ на виртуальной клавиатуре")


@user_reg.message(User.university, F.text)
async def get_uni(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()

    if message.text == "МГУ":
        if await insert_uni(message.from_user.id, Constants.MSU, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "ВШЭ":
        if await insert_uni(message.from_user.id, Constants.HSE, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "РАНХИГС":
        if await insert_uni(message.from_user.id, Constants.RANEPA, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "МГТУ им. Баумана":
        if await insert_uni(message.from_user.id, Constants.BMSTU, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "МИРЕА":
        if await insert_uni(message.from_user.id, Constants.MIREA, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    else:
        await message.answer("Выбери ответ на виртуальной клавиатуре")


@user_reg.message(User.age, F.text)
async def get_age(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
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
    connection_pool = await get_connection_pool()
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
            await state.set_state(User.image)
    except ValueError:
        await message.answer("Введи возраст числом")
    except IndexError:
        await message.answer("Введи возраст в формате YY-YY")


@user_reg.message(User.image, F.content_type.in_([F.PHOTO, F.VIDEO]))
async def get_album(message: types.Message, album: list[types.Message] = None, state: FSMContext = 0):
    connection_pool = await get_connection_pool()
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
    connection_pool = await get_connection_pool()
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


