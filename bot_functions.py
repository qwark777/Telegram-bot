import os
from collections import defaultdict
from email.errors import MessageDefect
from typing import List, Union

import aiomysql
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from dotenv import load_dotenv, find_dotenv

from clases import Constants, User
from databases_functions import select_name
from redis_functions import get_watched_profiles, add_watched_profiles, add_liked_profiles, get_liked_profiles
from reply import like_keyboard, like_wait_keyboard

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
users_data = defaultdict(list)

last_watched_form = defaultdict(lambda : 0)


async def print_profile(self_id: int, form: List[Union[int, str]]):
    text = str(os.getenv("FORM_PATTERN"))
    if form[18] == "":
        text = os.getenv("FORM_PATTERN_WITHOUT_DESC")
    text = text.format(NAME=form[1], AGE=form[4], DESC=form[18])
    media = list()
    if int(form[14]) == Constants.video:
        media.append(types.InputMediaVideo(media=form[10], caption=text))
    else:
        media.append(types.InputMediaPhoto(media=form[10], caption=text))
    for i in range(2, form[9] + 1):
        if int(form[13 + i]) == Constants.video:
            media.append(types.InputMediaVideo(media=form[9 + i]))
        else:
            media.append(types.InputMediaPhoto(media=form[9 + i]))

    await bot.send_media_group(self_id, media=media)
    await bot.send_message(self_id, text='Как тебе анкета?', reply_markup=like_keyboard)


async def get_any_profile(self_id: int, connection_pool: aiomysql.pool.Pool) -> None:
    if not users_data[self_id]:
        try:
            async with connection_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    string = os.getenv("SELECT_ALL")
                    string = string.format(ID=self_id)
                    await cursor.execute(string)
                    users_data[self_id] = (await cursor.fetchall())[0]
                    await conn.commit()
        except Exception as e:
            print(e, get_any_profile.__name__, 1)
    viewed_profiles = await get_watched_profiles(self_id)
    if viewed_profiles:
        placeholders = ', '.join(viewed_profiles)
        exclusion_query = f"AND id NOT IN ({placeholders})"
    else:
        exclusion_query = ""

    query = f"""
        SELECT * FROM users 
        WHERE id != {users_data[self_id][0]}
        AND age BETWEEN {users_data[self_id][5]} AND {users_data[self_id][6]} 
        AND university & {users_data[self_id][8]} != 0 
        AND sex & {users_data[self_id][3]} != 0
        AND sex_find & {users_data[self_id][2]} != 0
        {exclusion_query}
        ORDER BY RAND()
        LIMIT 1
        """
    try:
        async with connection_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                form = (await cursor.fetchall())
                if form:
                    form = form[0]
                    last_watched_form[self_id] = form[0]
                    await print_profile(self_id, form)
                else:
                    await bot.send_message(self_id, text='Эта была последняя анкета. Поменяй критерии поиска или начни заново')
                await conn.commit()
    except Exception as e:
        print(e, get_any_profile.__name__, 2)


async def like(self_id: int):
    if last_watched_form[self_id]:
        await bot.send_message(last_watched_form[self_id], text="Ты понравился одному пользователю. Покажем его анкету следующей", reply_markup=like_wait_keyboard)
        state_with = FSMContext(storage=dp.storage, key=StorageKey(user_id=last_watched_form[self_id], bot_id=bot.id, chat_id=last_watched_form[self_id]))
        await state_with.set_state(User.like_wait)
        await add_watched_profiles(self_id, last_watched_form[self_id])
        await add_liked_profiles(str(self_id) + 'l', last_watched_form[self_id])
    else:
        await bot.send_message(self_id, text="Время просмотра анкеты истекло")

async def dislike(self_id: int) -> bool:
    if last_watched_form[self_id]:
        await add_watched_profiles(self_id, last_watched_form[self_id])
        return True
    else:
        await bot.send_message(self_id, text="Время просмотра анкеты истекло")
        return False


async def create_inline_keyboard(button_texts: List[str]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=text, callback_data=f'btn_07_{i + 1}')] for i, text in enumerate(button_texts)]
    buttons.append([InlineKeyboardButton(text="Принять 👍", callback_data=f'btn_07_{100}')])
    buttons.append([InlineKeyboardButton(text="Назад 🔙", callback_data=f'btn_07_{99}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def delete_messages(message: Message, _id):
    try:
        await bot.edit_message_reply_markup(chat_id=_id, message_id=message.message_id, reply_markup=None)

    finally:
        await bot.session.close()


async def print_like_form(self_id: int, connection_pool: aiomysql.pool.Pool, state: FSMContext):
    number = await get_liked_profiles(str(self_id) + 'l')
    if number is None:
        await get_any_profile(self_id, connection_pool)
        await state.set_state(User.find)
        return
    last_watched_form[self_id] = number
    query = f"SELECT * FROM users WHERE id = {number}"
    try:
        async with connection_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                form = (await cursor.fetchall())
                form = form[0]
                last_watched_form[self_id] = form[0]
                await print_profile(self_id, form)
                await conn.commit()
    except Exception as e:
        print(e, get_any_profile.__name__)


async def get_username(chat_id: int):
    chat = await bot.get_chat(last_watched_form[chat_id])
    username = chat.username
    return username


async def print_username(chat_id: int, connection_pool: aiomysql.pool.Pool):
    chat = await bot.get_chat(chat_id)
    username = chat.username
    await bot.send_message(chat_id=chat_id, text=f"Ты понравился взаимно пользователю {select_name(chat_id, connection_pool)}\nВот тег в Телеграме: {username}")
    return username
