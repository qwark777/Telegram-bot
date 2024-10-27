from aiogram.fsm.state import StatesGroup, State
from typing import Callable, Any, Awaitable, Union, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
import asyncio

class Constants:
    guy = 1
    girl =  0
    someone = 2
    photo = 1
    video = 0

class User(StatesGroup):
    registration = State()  # желание зарегестрироваться
    name = State()
    age = State()
    sex = State()
    university = State()
    image = State()
    age_find = State()
    find_sex = State()
    description = State()
    wait = State()

class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.2):
        self.latency = latency

    async def __call__(self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], message: Message, data: dict[str, Any]) -> Any:

        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
        res = await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']
        return res


