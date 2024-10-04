from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True

)
