from telebot import types

#back to main menu button keyboard
back_to_main = types.InlineKeyboardMarkup(row_width=1)
item1 = types.InlineKeyboardButton("🔙 Вернуться в главное меню 🔙", callback_data='main_menu')
back_to_main.add(item1)

#main menu keyboard
main_menu = types.InlineKeyboardMarkup(row_width=1)
item1 = types.InlineKeyboardButton("Добавить memo 🆕", callback_data='start')
item2 = types.InlineKeyboardButton("Текущие memo 📜", callback_data='memos_list')
item3 = types.InlineKeyboardButton("Помощь 🚑", callback_data='help')
main_menu.add(item1, item2, item3)

#type select keyboard
type_select = types.InlineKeyboardMarkup(row_width=1)
item1 = types.InlineKeyboardButton("Текст 📝", callback_data='text')
item2 = types.InlineKeyboardButton("Фото(скоро 😢)", callback_data='photo_later')
item3 = types.InlineKeyboardButton("Файл(скоро 😭)", callback_data='file_later')
type_select.add(item1, item2, item3)