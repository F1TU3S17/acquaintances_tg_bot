from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton,InlineKeyboardMarkup)

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать рассылку')],[KeyboardButton(text='Просмотр жалоб')]],resize_keyboard=True)
send = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить')], [KeyboardButton(text='Отменить')]],resize_keyboard=True)
report = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Заблокировать анкету'), KeyboardButton(text='Далее'), KeyboardButton(text='Выйти')]], resize_keyboard=True)