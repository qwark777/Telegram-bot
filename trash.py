@user_reg.message(User.registration, F.text)
async def continue_registration_mes(message: types.Message, state: FSMContext):
    if message.text == "Да ✅" or message.text.lower() == "да" or message.text == "✅" or message.text.lower() == "yes":
        await message.answer("Как тебя называть?")
        await state.set_state(User.name)
    elif message.text == "Нет ❌" or message.text.lower() == "нет" or message.text == "❌" or message.text.lower() == "no":
        await message.answer("Напиши тогда, как захочешь)")
        await state.clear()
    else:
        await message.answer("Напиши мне 'да' или 'нет' или выбери ответ на виртуальной клавиатуре")




@user_reg.message(User.sex, F.text)
async def get_sex_mes(message: types.Message, state: FSMContext):
    if message.text.lower() == "девушка" or message.text == "Девушка 👩‍🎓" or message.text.lower() == "girl" or message.text == "👩‍🎓":
        if await insert_sex(message.from_user.id, Constants.girl, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    elif message.text.lower() == "парень" or message.text == "Парень 👨‍🎓" or message.text.lower() == "boy" or message.text == "👨‍🎓":
        if await insert_sex(message.from_user.id, Constants.guy, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Кого будем искать?", reply_markup=find_sex_keyboard)
            await state.set_state(User.find_sex)
    else:
        await message.answer("Пожалуйста напиши мне 'парень' или 'девушка' или выбери ответ на виртуальной клавиатуре")

@user_reg.message(User.find_sex, F.text)
async def get_find_sex_mes(message: types.Message, state: FSMContext):
    if message.text.lower() == "девушек" or message.text == "Девушек 👩‍🎓" or message.text.lower() == "girls" or message.text == "👩‍🎓":
        if await insert_sex_find(message.from_user.id, Constants.girl, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    elif message.text.lower() == "парней" or message.text == "Парней 👨‍🎓" or message.text.lower() == "boys" or message.text == "👨‍🎓":
        if await insert_sex_find(message.from_user.id, Constants.guy, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    elif message.text == "Без разницы 🤷‍♂️🤷‍♀️" or message.text.lower() == "без разницы" or message.text == "🤷‍♂️🤷‍♀️":
        if await insert_sex_find(message.from_user.id, Constants.someone, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Из какого ты университета?", reply_markup=uni_keyboard)
            await state.set_state(User.university)
    else:
        await message.answer("Пожалуйста напиши мне 'парней', 'девушек' или 'без разницы' или выбери ответ на виртуальной клавиатуре")

@user_reg.message(User.university, F.text)
async def get_uni(message: types.Message, state: FSMContext):
    if message.text == "МГУ":
        if await insert_uni(message.from_user.id, Constants.MSU, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "ВШЭ":
        if await insert_uni(message.from_user.id, Constants.HSE, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "РАНХИГС":
        if await insert_uni(message.from_user.id, Constants.RANEPA, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "МГТУ им. Баумана":
        if await insert_uni(message.from_user.id, Constants.BMSTU, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    elif message.text == "МИРЕА":
        if await insert_uni(message.from_user.id, Constants.MIREA, connection_pool):
            await message.answer("В боте произошла ошибка, напиши позже")
        else:
            await message.answer("Какой университет тебя интересует?", reply_markup=await create_inline_keyboard(button_texts))
            await state.set_state(User.find_university)
    else:
        await message.answer("Выбери ответ на виртуальной клавиатуре")
