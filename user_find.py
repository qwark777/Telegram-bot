import os
from collections import defaultdict

import aiomysql
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from clases import User
from redis_functions import get_watched_profiles

users_find = Router()
global connection_pool

users_data = defaultdict(list)

async def create_user_find_router(con_pool: aiomysql.pool.Pool):
    global connection_pool
    connection_pool = con_pool


@users_find.message(User.find)
async def print_profile(message: types.Message, state: FSMContext):
    if not users_data[message.from_user.id]:
        try:
            async with connection_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    string = os.getenv("SELECT_ALL")
                    string = string.format(ID=message.from_user.id)
                    await cursor.execute(string)
                    users_data[message.from_user.id] = await cursor.fetchall()
                    await conn.commit()
        except Exception as e:
            print(e)
    viewed_profiles = await get_watched_profiles(message.from_user.id)
    if viewed_profiles:
        placeholders = ', '.join(viewed_profiles)
        exclusion_query = f"AND id NOT IN ({placeholders})"
    else:
        exclusion_query = ""

    query = f"""
        SELECT * FROM users 
        WHERE age BETWEEN {users_data[message.from_user.id][5]} AND {users_data[message.from_user.id][6]} 
        AND university & {users_data[message.from_user.id][8]} != 0 
        {exclusion_query}
        ORDER BY RAND() 
        LIMIT 1
        """
    try:
        async with connection_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                form = await cursor.fetchall()
                await conn.commit()
    except Exception as e:
        print(e)