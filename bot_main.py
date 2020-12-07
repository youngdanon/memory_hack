import config
from users import User
from memo import Memo
import file_saver
from db_controller import DB

import telebot
from telebot import types


import datetime

bot = telebot.TeleBot(config.TOKEN)

db = DB('./data/memos.db')
db.create_table()


test_notify_delta = [datetime.timedelta(hours=0, minutes=0, seconds=10),
                    datetime.timedelta(hours=0, minutes=0, seconds=30),
                    datetime.timedelta(hours=0, minutes=1, seconds=0)]


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
                     parse_mode="html", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def main_logic(call):
    if call.data:
        if call.data == 'help':
            bot.answer_callback_query(callback_query_id=call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Добавить memo", callback_data='start')
            markup.add(item1)

            help_text = open('help.txt', 'r', encoding='utf-8')
            bot.send_message(call.message.chat.id, help_text, reply_markup=markup)

        if call.data == 'start':
            bot.answer_callback_query(callback_query_id=call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Текст", callback_data='text')
            item2 = types.InlineKeyboardButton("Фото", callback_data='photo')
            item3 = types.InlineKeyboardButton("Файл", callback_data='file')
            markup.add(item1, item2, item3)
            bot.send_message(call.message.chat.id, "Окей, начинаем\n<b>Выбери тип memo:</b>",
                             parse_mode="html", reply_markup=markup)

        if call.data == 'text':
            bot.answer_callback_query(callback_query_id=call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Вернуться назад", callback_data='start')
            markup.add(item1)

            bot.send_message(call.message.chat.id, "Тип выбран.\n<b>Пришли мне текст одним сообщением</b>", parse_mode='html', reply_markup=markup)

            @bot.message_handler()
            def text_grabber(message):
                if message.chat.id == call.message.chat.id:
                    if message.text:
                        path = file_saver.save_txt(call.message.chat.id, message.text)
                        next_notify_time = datetime.datetime.now() + test_notify_delta[0]
                        new_memo = Memo(user_id=message.chat.id,
                                        memo_type="text", 
                                        link=path,
                                        notify_time=next_notify_time,
                                        notify_count=0)
                        user = User(message.chat.id)
                        user.add_memo(new_memo=new_memo)
                    # else:
                    #     markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
                    #     item1 = types.InlineKeyboardButton("Вернуться назад", callback_data='text')
                    #     markup.add(item1)
                    #     bot.send_message(message.chat.id, "Это не текст!\n<b>Попробуйте ещё раз!</b>", parse_mode='html', reply_markup = markup)
bot.polling(none_stop=True, interval=0)
