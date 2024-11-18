import asyncio
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


class Constants:
    guy = 1
    girl =  0
    someone = 2
    photo = 1
    video = 0
    MSU = 1
    HSE = 2
    RANEPA = 3
    BMSTU = 4
    MIREA = 5

class Patterns:
    MSU = 0b1
    HSE = 0b10
    RANEPA = 0b100
    BMSTU = 0b1000
    MIREA = 0b10000

class User(StatesGroup):
    registration = State()  # желание зарегестрироваться
    name = State()
    age = State()
    sex = State()
    university = State()
    find_university = State()
    image = State()
    age_find = State()
    find_sex = State()
    description = State()
    wait = State()
    find = State()
    like = State()
    returned = State()


class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}
    def __init__(self, latency: Union[int, float] = 0.2):
        self.latency = latency
    async def __call__(self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], message: Message, data: dict[str, Any]) -> Any:
        if message.media_group_id:
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
        else:
            data['album'] = [message]
            res = await handler(message, data)
        return res