import App.user_keyboards as kb

from aiogram.types import BufferedInputFile, ReplyKeyboardRemove
from BotData.database_function import *
from geopy.geocoders import Nominatim

# Функция для определения города, области, округа и страны по широте и долготе
def get_location_details(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language='ru')
    address = location.raw['address']

    city = address.get('city', '')
    if not city:
        city = address.get('town', '')
    if not city:
        city = address.get('village', '')
    if not city:
        city = address.get('hamlet', '')

    state = address.get('state', '')
    region = address.get('region', '')
    country = address.get('country', '')

    state_list = ['Донецкая область', 'Луганская область', 'Автономная Республика Крым']
    if state in ['Республика Крым', 'Херсонская область', 'Запорожская область']:
        country = 'Россия'
        region = 'Южный федеральный округ'
    elif state in state_list:
        country = 'Россия'
        if state == state_list[0]:
            state = 'Донецкая Народная Республика'
        elif state == state_list[1]:
            state = 'Луганская Народная Республика'
        else:
            state = 'Республика Крым'
        region = 'Южный федеральный округ'

    location_list = [city, state, region, country]
    return location_list

#city, state, region, country = get_location_details(latitude, longitude)
# Функция для определения города, области, округа и страны по названию города
def get_city_details(city_name):
    geolocator = Nominatim(user_agent="GetLoc")

    location = geolocator.geocode(city_name, addressdetails=True, language='ru')

    if location:
        address = location.raw.get('address', {})

        city = address.get('city', '')
        if not city:
            city = address.get('town', '')
        if not city:
            city = address.get('village', '')
        if not city:
            city = address.get('hamlet', '')

        state = address.get('state', '')
        region = address.get('region', '')
        country = address.get('country', '')

        state_list = ['Донецкая область', 'Луганская область', 'Автономная Республика Крым']
        if state in ['Республика Крым', 'Херсонская область', 'Запорожская область']:
            country = 'Россия'
            region = 'Южный федеральный округ'
        elif state in state_list:
            country = 'Россия'
            if state == state_list[0]:
                state = 'Донецкая Народная Республика'
            elif state == state_list[1]:
                state = 'Луганская Народная Республика'
            else:
                state = 'Республика Крым'
            region = 'Южный федеральный округ'

        location_list = [city, state, region, country]
        return location_list
    else:
        return []

#Функция для отправки пользователю его анкеты
async def send_form_to_user(bot, user_id: int, reply_markup=kb.form_menu()):
    photo_bytes = get_photo(user_id)
    list_info_about_user = await get_all_info(user_id)
    name = list_info_about_user[3]
    age = list_info_about_user[4]
    description = list_info_about_user[7] if str(list_info_about_user[7]) != 'None' else ""
    city = list_info_about_user[9]
    state = list_info_about_user[10]
    region = list_info_about_user[11]
    country = list_info_about_user[12]
    caption = str(f"{name}, {age}, {city}\n"
               f"{description}")
    input_file = BufferedInputFile(photo_bytes, filename='image.jpg')
    await bot.send_photo(chat_id=user_id, photo=input_file, caption=caption, reply_markup=reply_markup)

#Функция для отправки пользователю анкет возможных партнеров
async def send_partner_form_to_user(bot, user_id: int, partner_id: int, reply_markup=kb.form_menu(), is_view_like = False):
    photo_bytes = get_photo(partner_id)
    list_info_about_user = await get_all_info(partner_id)
    name = list_info_about_user[3]
    age = list_info_about_user[4]
    description = list_info_about_user[7] if str(list_info_about_user[7]) != 'None' else ""
    city = list_info_about_user[9]
    state = list_info_about_user[10]
    region = list_info_about_user[11]
    country = list_info_about_user[12]
    caption = str(f"{name}, {age}, {city}\n"
               f"{description}")
    input_file = BufferedInputFile(photo_bytes, filename='image.jpg')
    if is_view_like:
        message_to = await message_to_user(partner_id, user_id)
        if message_to != None:
            caption += f'\nСООБЩЕНИЕ ДЛЯ ВАС💌:\n{message_to}\n'
    await bot.send_photo(chat_id=user_id, photo=input_file, caption=caption, reply_markup=reply_markup)

#Функция для получения фотографии пользователя из телеграмма
async def take_user_photo_tg(bot, user_id):
    user_photos = await bot.get_user_profile_photos(user_id)
    if user_photos:
        first_photo = user_photos.photos[0][-1]
        file_info = await bot.get_file(first_photo.file_id)
        file_path = file_info.file_path
        photo = await bot.download_file(file_path)
        return photo
    return None

#Функция отправляется информацию с количеством симпатий у пользователя
async def send_like(bot, partner_id):
    counter = await like_counts(partner_id)
    if counter:
        message = f"Вам выразили симпатию {counter} человек"
        await bot.send_message(partner_id, message, reply_markup=kb.shows_more)


#Функция отправляет username и анкету пользвателя, если совпала симпатия пользователю с id user_id
async def send_username_to_partner(bot, user_id, from_user_id, username):
    await bot.send_message(user_id, f'У вас с @{username} взаимная симпатия, если забыл кто это, вот анкета')
    await send_partner_form_to_user(bot, user_id, from_user_id, ReplyKeyboardRemove())

