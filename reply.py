from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="Да ✅"),
            KeyboardButton(text="Нет ❌")
        ]
    ],
    resize_keyboard=True

)
del_keyboard = ReplyKeyboardRemove()

sex_keyboard = ReplyKeyboardMarkup(
    keyboard =
    [
        [
            KeyboardButton(text="Парень 👨‍🎓"),
            KeyboardButton(text="Девушка 👩‍🎓")
        ]
    ],
    resize_keyboard=True
)
find_sex_keyboard = ReplyKeyboardMarkup(
    keyboard =
    [
        [
            KeyboardButton(text="Парень 👨‍🎓"),
            KeyboardButton(text="Девушка 👩‍🎓")
        ],
        [
            KeyboardButton(text="Без разницы 🤷‍♂️🤷‍♀️")
        ]
    ],
    resize_keyboard=True
)