import telebot
import asyncio

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "соси хуй Леша")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot = telebot.TeleBot("7061086759:AAF_s5oDahOFyjojIVMTGnyU-BEJjxEkgdA")
bot.polling(none_stop=True, interval=0)
