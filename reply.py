from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Да ✅", callback_data="btn_01_01"),
            InlineKeyboardButton(text="Нет ❌", callback_data="btn_01_02")
        ]
    ]
)

del_keyboard = ReplyKeyboardRemove()

sex_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Парень 👨‍🎓", callback_data="btn_02_01"),
            InlineKeyboardButton(text="Девушка 👩‍🎓", callback_data="btn_02_02")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="btn_02_99")
        ]
    ]
)

find_sex_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Парней 👨‍🎓", callback_data="btn_03_01"),
            InlineKeyboardButton(text="Девушек 👩‍🎓", callback_data="btn_03_02")
        ],
        [
            InlineKeyboardButton(text="Без разницы 🤷‍♂️🤷‍♀️", callback_data="btn_03_03")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="btn_03_99")
        ]
    ]
)

age_back = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад 🔙', callback_data='btn_05_99')
        ]
    ]
)

age_find_back = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад 🔙', callback_data='btn_06_99')
        ]
    ]
)

media_back = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад 🔙', callback_data='btn_08_99')
        ]
    ]
)

wait_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Да ✅", callback_data="btn_09_01"),
            InlineKeyboardButton(text="Нет ❌", callback_data="btn_09_02")
        ]
    ]
)

uni_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="МГУ", callback_data="btn_04_01")],
        [InlineKeyboardButton(text="ВШЭ", callback_data="btn_04_02")],
        [InlineKeyboardButton(text="РАНХИГС", callback_data="btn_04_03")],
        [InlineKeyboardButton(text="МГТУ им. Баумана", callback_data="btn_04_04")],
        [InlineKeyboardButton(text="МИРЕА", callback_data="btn_04_05")],
        [InlineKeyboardButton(text="Назад 🔙", callback_data="btn_04_99")]
    ]
)

button_texts = ["МГУ ✅", "ВШЭ ✅", "РАНХИГС ✅", "МГТУ им. Баумана ✅", "МИРЕА ✅"]


returned_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Да ✅", callback_data="btn_10_01"),
            InlineKeyboardButton(text="Нет ❌", callback_data="btn_10_02")
        ]
    ]
)

like_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Нравится 🩷", callback_data="btn_11_01"),
            InlineKeyboardButton(text="Не нравится 🚫", callback_data="btn_11_02")

        ],
        [
            InlineKeyboardButton(text="Отложить 🤷‍♂️", callback_data="btn_11_03"),
            InlineKeyboardButton(text="Анонимный лайк 🖤", callback_data="btn_11_04"),
        ],
        [
            InlineKeyboardButton(text="Сообщение 💌", callback_data="btn_11_05"),
            InlineKeyboardButton(text="Меню 💤", callback_data="btn_11_06"),
        ],
        [
            InlineKeyboardButton(text="Пожаловаться ‼️", callback_data="btn_11_07")
        ]
    ]
)


like_wait_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Да ✅", callback_data="btn_13_01"),
            InlineKeyboardButton(text="Продолжить просмотр анкет ❌", callback_data="btn_13_02")
        ]
    ]
)

ban_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="БАН ‼️", callback_data="btn_99_01"),
            InlineKeyboardButton(text="НОРМ ✅", callback_data="btn_99_02")
        ]
    ]
)

meny_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Анкеты 👀", callback_data="btn_14_01"),
            InlineKeyboardButton(text="Изменить анкету ✏️", callback_data="btn_14_02")
        ],
        [
            InlineKeyboardButton(text="Отключить анкету 📴", callback_data="btn_14_03")
        ]
    ]
)

message_back = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад 🔙', callback_data='btn_15_99')
        ]
    ]
)