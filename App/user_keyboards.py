from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton,InlineKeyboardMarkup)
from BotData.database_function import *


start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать анкету')]],
                            resize_keyboard=True)

from_tg = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Взять из телеграмма')]],
                                   resize_keyboard=True)

def age(tg_id):
    keyboard = []
    age = str(get_age(tg_id))
    if age != None:
        keyboard.append([KeyboardButton(text=age)])
    return ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True)



sex = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Парень'), KeyboardButton(text='Девушка')]],
                          resize_keyboard=True)


interest = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Парни'), KeyboardButton(text='Девушки'),
                                          KeyboardButton(text='Все равно')]], resize_keyboard=True)


def description(tg_id):
    keyboard = [[KeyboardButton(text='Пропустить')]]
    description_exist = get_description(tg_id)
    if description_exist != None:
        keyboard.append([KeyboardButton(text='Оставить текущее')])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


confirm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Подтвердить'), KeyboardButton(text='Отменить')]],
                              resize_keyboard=True)


def location(tg_id):
    keyboard = [[KeyboardButton(text='Предоставить геолокацию📍', request_location=True)]]
    city = get_city(tg_id)
    if city:
        keyboard.append([KeyboardButton(text=city)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def photo(tg_id):
    keyboard = [[KeyboardButton(text='Взять из телеграмма')]]
    photo_exist = get_photo(tg_id)
    if photo_exist != None:
        keyboard.append([KeyboardButton(text='Взять текущее фото')])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def form_menu():
    edit_form = [InlineKeyboardButton(text='Изменить данные в анкете', callback_data=f'edit_form')]
    edit_photo = [InlineKeyboardButton(text='Изменить фото', callback_data='edit_photo')]
    edit_search = [InlineKeyboardButton(text='Настроить детали поиска', callback_data=f'edit_search')]
    edit_active = [InlineKeyboardButton(text='Активность анкеты', callback_data=f'edit_active')]
    keyboard = [edit_form, edit_photo, edit_active]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_setting():
    edit_all_from = [InlineKeyboardButton(text='Заполнить анкету заново', callback_data='edit_all')]
    edit_name = [InlineKeyboardButton(text='Изменить имя', callback_data='edit_name')]
    edit_age = [InlineKeyboardButton(text='Изменить возраст', callback_data='edit_age')]
    edit_sex = [InlineKeyboardButton(text='Изменить пол', callback_data='edit_sex')]
    edit_description = [InlineKeyboardButton(text='Изменить описание профиля', callback_data='edit_desc')]
    edit_location = [InlineKeyboardButton(text='Изменить местоположение', callback_data='edit_location')]
    back = [InlineKeyboardButton(text='Назад', callback_data='back_menu')]
    keyboard = [edit_all_from, edit_name, edit_age, edit_sex, edit_location, edit_description, back]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_search_detail():
    edit_sex_search = [InlineKeyboardButton(text='Изменить пол поиска', callback_data='search_sex')]
    edit_location_search = [InlineKeyboardButton(text='Настроить область поиска', callback_data='search_location')]
    back = [InlineKeyboardButton(text='Назад', callback_data='back_menu')]
    keyboard = [edit_location_search, edit_sex_search, back]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def form_search_location():
    city = [InlineKeyboardButton(text='Искать в моем городе',callback_data='search_city')]
    state = [InlineKeyboardButton(text='Искать в моей области', callback_data='search_state')]
    region = [InlineKeyboardButton(text='Искать моем округе', callback_data='search_region')]
    country = [InlineKeyboardButton(text='Искать моей стране', callback_data='search_country')]
    back = [InlineKeyboardButton(text='Назад', callback_data='back_search')]
    keyboard = [city, state, region, country, back]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_active(tg_id):
    on = [InlineKeyboardButton(text='Активировать анкету', callback_data='edit_on')]
    off = [InlineKeyboardButton(text='Отключить анкету', callback_data='edit_off')]
    back = [InlineKeyboardButton(text='Назад', callback_data='back_menu')]
    keyboard = []
    is_active = get_active(tg_id)
    if is_active:
        keyboard.append(off)
        keyboard.append(back)
    else:
        keyboard.append(on)
        keyboard.append(back)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

scroll = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❤️'),KeyboardButton(text='❌'),KeyboardButton(text='💌')],
                                        [KeyboardButton(text='Отправить жалобу')],
                                        [KeyboardButton(text='Выйти из поиска')]
                                        ],
                                   resize_keyboard=True)

start_search = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать поиск')]], resize_keyboard=True)

shows_more = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Посмотреть все', callback_data='shows_more')]])

undo = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отменить')]],resize_keyboard=True)

view_like = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❤️'),KeyboardButton(text='❌')],[KeyboardButton(text='Выйти из просмотра')]],
                                   resize_keyboard=True)
