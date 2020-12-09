import config
from users import User, return_overdue_memos
from memo import Memo
import file_saver
from db_controller import DB
import file_reader

import telebot
from telebot import types
import keyboards

import datetime
import time
import threading

bot = telebot.TeleBot(config.TOKEN)

db = DB('./data/memos.db')
db.create_table()

memo_name = {}


test_notify_delta = [datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5)]
notify_delta = [datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5),
                    datetime.timedelta(hours=0, minutes=0, seconds=5)]


def time_checker():
    memo_list = return_overdue_memos(datetime.datetime.now())
    for memo in memo_list:
        if memo.memo_type == 'text':
            text = f"Время повторить 🧠\n<b><i>{memo.memo_name}</i>(Текстовый)</b>\n\n{file_reader.txt_read(memo.link)}"
            bot.send_message(memo.user_id, text, parse_mode='html', reply_markup=keyboards.back_to_main)
            memo.notify_time += test_notify_delta[memo.notify_count + 1]
            memo.notify_count += 1
            if memo.notify_count >= 5:
                bot.send_message(memo.user_id, f"<b>Memo <i>{memo.memo_name}</i></b> закреплен в вашей памяти надолго.", parse_mode='html', reply_markup=keyboards.back_to_main)
            else:
                user = User(memo.user_id)
                user.add_memo(new_memo=memo)
            
        elif memo.memo_type == 'file':
            pass
        else:
            pass
    print(time.ctime(), "(time_checker)")
    threading.Timer(3, time_checker).start()

time_checker()

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
    if call.data == 'main_menu':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.send_message(call.message.chat.id, "<b>Главное меню</b>",
                        parse_mode="html", reply_markup=keyboards.main_menu)
                        
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
            
        bot.send_message(call.message.chat.id, parsed_memo_list + "\n\n\n<b>Твои текущие memo ↑</b>", parse_mode='html', reply_markup=keyboards.back_to_main)


    if call.data == 'help':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        help_text = file_reader.txt_read('help.txt')
        bot.send_message(call.message.chat.id, help_text, parse_mode="html", reply_markup=keyboards.back_to_main)

    if call.data == 'start':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.send_message(call.message.chat.id, "Окей, начинаем\n<b>Выбери тип memo:</b>",
                            parse_mode="html", reply_markup=keyboards.type_select)

    if call.data == 'text':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        msg = bot.send_message(call.message.chat.id, "Тип выбран✅\n<b>Назовите свой memo</b>", parse_mode='html', reply_markup=keyboards.back_to_main)
        bot.register_next_step_handler(msg, text_memo_naming)

    if call.data == 'file':
        bot.answer_callback_query(callback_query_id=call.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        msg = bot.send_message(call.message.chat.id, "Тип выбран✅\n<b>Назовите свой memo</b>", parse_mode='html', reply_markup=keyboards.back_to_main)
        bot.register_next_step_handler(msg, file_memo_naming)

        
        
def text_memo_naming(message):
    global memo_name
    
    if message.text:
        
        memo_name.update({message.chat.id : message.text})
        print(memo_name)
        
        msg = bot.send_message(message.chat.id, "Классное название😋\n<b>Пришли мне текст одним сообщением</b>📝", parse_mode='html', reply_markup=keyboards.back_to_main)
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

        bot.send_message(message.chat.id, "✅<b>Мемо успешно создан</b>✅\n"
        "Включи уведомления и я буду присылать тебе напоминания⏰", parse_mode='html', reply_markup=keyboards.back_to_main)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def file_memo_naming(message):
    global memo_name
    
    if message.text:
        memo_name.update({message.chat.id : message.text})
        print(memo_name,"(document detected)")

        msg = bot.send_message(message.chat.id, "Классное название.\n<b>Прикрепи 1 файл в следующем сообщении</b>", parse_mode='html', reply_markup=keyboards.back_to_main)
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

        bot.send_message(message.chat.id, "<b>Мемо успешно создан.</b>\n"
        "Включи уведомления и я буду присылать тебе напоминания.", parse_mode='html', reply_markup=keyboards.back_to_main)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True, interval=0)