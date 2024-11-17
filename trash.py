@user_reg.callback_query(User.find_university, lambda c: c.data and c.data.startswith('btn'))
async def keyboard_handler(callback_query: types.CallbackQuery, state: FSMContext):
    index = int(callback_query.data.split("_")[-1])
    if index  == 100:
        await callback_query.message.answer("Сколько тебе лет?")
        await state.set_state(User.age)
    elif index  == 99:
        pass
    else:
        if find_uni[callback_query.from_user.id][index-1][-1] == '❌':
            char = '✅'
        else:
            char = '❌'
        find_uni[callback_query.from_user.id][index-1] = f"{find_uni[callback_query.from_user.id][index-1][:-1]}{char}"
        try:
            await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=await create_inline_keyboard(find_uni[callback_query.from_user.id]))
        except Exception as e:
            print(e)

    await bot.answer_callback_query(callback_query.id)


@user_reg.callback_query(lambda c: c.data and c.data == 'btn_99')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    pass


# @user_reg.message(Command("profile"), F.text)
# async def print_profile(message: types.Message, state: FSMContext):
#     connection_pool = await get_connection_pool()
#     await print_registration_profile(message.from_user.id, connection_pool, bot)