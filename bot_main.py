import config

import telebot
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Добавить memo", callback_data='start')
    item2 = types.InlineKeyboardButton("Как пользоваться", callback_data='help')
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     " твой лучший помощник по запоминанию информации!".format(
                         message.from_user, bot.get_me()),
                     parse_mode="html")
    bot.send_message(message.chat.id,
                     "Давай начнем".format(
                         message.from_user, bot.get_me()),
                     parse_mode="html", reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True)
def main_logic(call):
  if call.data:
    if call.data == 'start':
      bot.answer_callback_query(callback_query_id=call.id)
      bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

      markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
      item1 = types.InlineKeyboardButton("Текст", callback_data='text')
      item2 = types.InlineKeyboardButton("Фото", callback_data='photo')
      item3 = types.InlineKeyboardButton("Файл", callback_data='file')
      markup.add(item1, item2, item3)
      bot.send_message(call.message.chat.id, "Окей, начинаем\n<b>Выбери тип memo:</b>", parse_mode="html",
                        reply_markup=markup)




bot.polling(none_stop=True, interval=0)