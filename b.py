document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)
    await message.answer_photo(file_info.file_id)