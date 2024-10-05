from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="Да ✅"),
            KeyboardButton(text="Нет ❎")
        ]
    ],
    resize_keyboard=True

)
del_keyboard = ReplyKeyboardRemove()
