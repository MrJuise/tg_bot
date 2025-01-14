from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb_in = InlineKeyboardMarkup()
but_start = KeyboardButton(text="Перевести")
but_start1 = KeyboardButton(text="Информация о боте")

in_button = InlineKeyboardButton(text='Перевод бота', callback_data="trans_bot")
in_button1 = InlineKeyboardButton(text='Перевод GigaChat', callback_data="trans_giga")

kb.row(but_start, but_start1)
kb_in.row(in_button, in_button1)
