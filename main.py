import asyncio
import aiomysql


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from admins_router import create_admin_router, admin_router
from bot_functions import bot, dp, start_message, end_message
from clases import AlbumMiddleware
from redis_functions import init_redis
from scheduler import delete_inactive_users
from user_find_router import users_find, create_user_find_router
from users_reg_router import user_reg, create_user_router


dp.message.middleware(AlbumMiddleware())
dp.include_router(user_reg)
dp.include_router(users_find)
dp.include_router(admin_router)




async def main():
    # dp.startup.register(start_message)
    # dp.shutdown.register(end_message)
    await init_redis()
    connection_pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='msutndr', minsize=1, maxsize=100)
    await create_user_router(connection_pool)
    await create_user_find_router(connection_pool)
    await create_admin_router(connection_pool)
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_inactive_users, args=[connection_pool], trigger='cron', hour=0, minute=0)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
