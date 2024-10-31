from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

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
            KeyboardButton(text="Парней 👨‍🎓"),
            KeyboardButton(text="Девушек 👩‍🎓")
        ],
        [
            KeyboardButton(text="Без разницы 🤷‍♂️🤷‍♀️")
        ]
    ],
    resize_keyboard=True
)

find_university = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='МГУ ❌', callback_data='МГУ'),
            InlineKeyboardButton(text='ВШЭ ❌', callback_data='ВШЭ'),
            InlineKeyboardButton(text='РАНХИГС ❌', callback_data='РАНХИГС'),
            InlineKeyboardButton(text='МГТУ им. Баумана ❌', callback_data='МГТУ'),
            InlineKeyboardButton(text='МИРЕА ❌', callback_data='МИРЕА')
        ]
    ]
)

