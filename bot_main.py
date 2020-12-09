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

memo_name = {}

test_notify_delta = [datetime.timedelta(hours=0, minutes=0, seconds=10),
                    datetime.timedelta(hours=0, minutes=0, seconds=30),
                    datetime.timedelta(hours=0, minutes=1, seconds=0)]

def naming_mssg(chat_id):
    bot.send_message(chat_id,"<b>Вы успешно назвали свой memo!</b>", parse_mode="html")



@bot.message_handler(commands=['start'])
def welcome(message):
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Начать", callback_data='main_menu')
    markup.add(item1)
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
        if call.data == 'main_menu':
            bot.answer_callback_query(callback_query_id=call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Добавить memo", callback_data='start')
            item2 = types.InlineKeyboardButton("Текущие memo", callback_data='memos_list')
            item3 = types.InlineKeyboardButton("Помощь", callback_data='help')
            markup.add(item1, item2, item3)
            bot.send_message(call.message.chat.id, "-------------------------\n<b>Главное меню</b>",
                            parse_mode="html", reply_markup=markup)
    if call.data:
        if call.data == 'memos_list':
            bot.answer_callback_query(callback_query_id=call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            user = User(call.message.chat.id)
            memo_list = user.get_memos_list()
            parsed_memo_list = ""
            for memo in memo_list:
                if memo.memo_type == 'text':
                    type_str = "Текстовый memo"
                elif memo.memo_type == 'photo':
                    type_str = "Фото-memo"
                else:
                    type_str = "Файловый memo"
                parsed_memo_list +=  f"======================\n{type_str}\n<b>{memo.memo_name}</b>\nСлед. повторение: {memo.notify_time}\nПовторено (раз): {memo.notify_count}\n"

            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Назад", callback_data='main_menu')
            markup.add(item1)
                
            bot.send_message(call.message.chat.id, parsed_memo_list + "\n\n\n<b>Твои текущие memo ↑</b>", parse_mode='html', reply_markup=markup)


    if call.data == 'help':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Назад", callback_data='main_menu')
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
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)

        msg = bot.send_message(call.message.chat.id, "Тип выбран.\n<b>Назовите свой memo</b>", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, text_memo_naming)

    if call.data == 'file':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)

        msg = bot.send_message(call.message.chat.id, "Тип выбран.\n<b>Назовите свой memo</b>", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, file_memo_naming)

        
        
def text_memo_naming(message):
    global memo_name
    
    if message.text:
        
        memo_name.update({message.chat.id : message.text})
        print(memo_name)
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)
        
        msg = bot.send_message(message.chat.id, "Классное название.\n<b>Пришли мне текст одним сообщением</b>", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, text_recieve)


def text_recieve(message):
    
    if message.text:
        path = file_saver.save_txt(message.chat.id, message.text)
        next_notify_time = datetime.datetime.now() + test_notify_delta[0]
        new_memo =  Memo(user_id=message.chat.id,
                            memo_type="text", 
                            memo_name=memo_name.pop(message.chat.id),
                            link=path,
                            notify_time=next_notify_time,
                            notify_count=0)
        user = User(message.chat.id)
        user.add_memo(new_memo=new_memo)

        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)

        bot.send_message(message.chat.id, "<b>Мемо успешно создан.</b>\n"
        "Включи уведомления и я буду присылать тебе напоминания.", parse_mode='html', reply_markup=markup)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def file_memo_naming(message):
    global memo_name
    
    if message.text:
        memo_name.update({message.chat.id : message.text})
        print(memo_name,"(document detected)")
        
        
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)

        msg = bot.send_message(message.chat.id, "Классное название.\n<b>Прикрепи 1 файл в следующем сообщении</b>", parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, file_recieve)


def file_recieve(message):
    
    if message.document:
        path = file_saver.save_file(message.chat.id, message.text)
        next_notify_time = datetime.datetime.now() + test_notify_delta[0]
        new_memo =  Memo(user_id=message.chat.id,
                            memo_type="text", 
                            memo_name=memo_name.pop(message.chat.id),
                            link=path,
                            notify_time=next_notify_time,
                            notify_count=0)
        user = User(message.chat.id)
        user.add_memo(new_memo=new_memo)

        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Вернуться в главное меню", callback_data='main_menu')
        markup.add(item1)

        bot.send_message(message.chat.id, "<b>Мемо успешно создан.</b>\n"
        "Включи уведомления и я буду присылать тебе напоминания.", parse_mode='html', reply_markup=markup)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True, interval=0)