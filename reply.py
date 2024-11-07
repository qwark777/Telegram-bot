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


back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад 🔙', callback_data='btn_99')
        ]
    ]
)


uni_keyboard = ReplyKeyboardMarkup(
    keyboard =
    [
        [
            KeyboardButton(text="МГУ"),
            KeyboardButton(text="ВШЭ")
        ],
        [
            KeyboardButton(text="РАНХИГС"),
            KeyboardButton(text="МГТУ им. Баумана")
        ],
        [
            KeyboardButton(text="МИРЕА")
        ]
    ],
    resize_keyboard=True
)

button_texts = ["МГУ ✅", "ВШЭ ✅", "РАНХИГС ✅", "МГТУ им. Баумана ✅", "МИРЕА ✅"]