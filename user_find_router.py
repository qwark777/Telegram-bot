import aiomysql
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from bot_functions import get_any_profile, bot, dislike, like, print_like_form, get_username, print_username, anon_like, \
    ban_profile
from clases import User, Admin
from reply import meny_keyboard

storage = MemoryStorage()
users_find = Router()
global connection_pool


async def create_user_find_router(con_pool: aiomysql.pool.Pool):
    global connection_pool
    connection_pool = con_pool


@users_find.callback_query(User.find, lambda c: c.data and c.data.startswith('btn_11_'))
async def print_find_profile(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 2:
        await dislike(callback_query.from_user.id)
        await get_any_profile(callback_query.from_user.id, connection_pool)
    elif index == 1:
        await like(callback_query.from_user.id, connection_pool)
        await get_any_profile(callback_query.from_user.id, connection_pool)
    elif index == 3:
        await get_any_profile(callback_query.from_user.id, connection_pool)
    elif index == 4:
        await anon_like(callback_query.from_user.id)
        await get_any_profile(callback_query.from_user.id, connection_pool)
    elif index == 6:
        await state.set_state(User.menu)
        await callback_query.message.answer("Меню", reply_markup=meny_keyboard)
    elif index == 5:
        pass
    elif index == 7:
        await callback_query.message.answer('Жалоба принята ✅')
        await ban_profile(callback_query.from_user.id, connection_pool)
        await bot.send_message(Admin.admin_chat, )
    await bot.answer_callback_query(callback_query.id)


@users_find.callback_query(User.like_wait, lambda c: c.data and c.data.startswith('btn_13_'))
async def wait_like_from(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index == 1:
        await state.set_state(User.like)
        await print_like_form(callback_query.from_user.id, connection_pool, state)
    elif index == 2:
        await state.set_state(User.find)
        await get_any_profile(callback_query.from_user.id, connection_pool)
    await bot.answer_callback_query(callback_query.id)



@users_find.callback_query(User.like, lambda c: c.data and c.data.startswith('btn_11_'))
async def like_form(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    try:
        if index == 1:
            if await dislike(callback_query.from_user.id):
                await callback_query.message.answer(f"Отлично, лови тег в Телеграме: @{await get_username(callback_query.from_user.id)}")
                await print_username(callback_query.from_user.id, connection_pool)
            await print_like_form(callback_query.from_user.id, connection_pool, state)
        elif index == 2:
            await dislike(callback_query.from_user.id)
            await print_like_form(callback_query.from_user.id, connection_pool, state)
        await bot.answer_callback_query(callback_query.id)
    except Exception as e:
        print(e)