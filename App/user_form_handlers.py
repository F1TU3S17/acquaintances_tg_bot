import App.user_keyboards as kb
from BotData.database_function import *
from BotData.config import bot_token
from App.states import *
from .function import *

from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

bot = Bot(token=bot_token)
router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    user = message.from_user
    user_id = user.id
    is_exist = await check_id(user_id)
    if not(is_exist):
        await message.answer('Привет! Это бот для знакомств, чтобы начать поиск новых знакомств, стоит создать анкету!'
                                 ,reply_markup=kb.start)
    else:
        await send_form_to_user(bot, user_id)
        await message.answer('Чтобы начать поиск, всего лишь нажми на кнопку!', reply_markup=kb.start_search)

@router.message(F.text == 'Создать анкету')
async def start_form(message: Message, state: FSMContext):
    await message.answer('Введите ваше имя', reply_markup=kb.from_tg)
    await state.set_state(form.name)

@router.message(form.name)
async def name_from_user(message: Message, state: FSMContext):
    user = message.from_user
    if (message.text == 'Взять из телеграмма'):
        user_name = user.first_name
        await state.update_data(name=user_name)
    else:
        await state.update_data(name=message.text)

    user_id = user.id
    if get_age(user_id) != None:
        await message.answer('Введите ваш возраст', reply_markup=kb.age(user_id))
    else:
        await message.answer('Введите ваш возраст',reply_markup=ReplyKeyboardRemove())
    await state.set_state(form.age)


@router.message(form.age)
async def age_from_user(message: Message, state:FSMContext):
    age = message.text
    try:
        age = int(age)
        if age > 12:
            await state.update_data(age=age)
            await message.answer('Выберите ваш пол', reply_markup=kb.sex)
            await state.set_state(form.sex)
        else:
            await message.answer('Извините, ботом можно пользоваться, только, если вам больше 12')
    except ValueError:
        await message.answer('Это не возраст!!!')


@router.message(form.sex)
async def sex_from_user(message: Message, state:FSMContext):
    sex = ['Парень', 'Девушка']
    if not(message.text in sex):
        await message.answer('Такого варианта нет...')
    else:
        index = sex.index(message.text)
        await state.update_data(sex=index)
        await message.answer('Теперь выбери, кто тебя интересует', reply_markup=kb.interest)
        await state.set_state(form.interest)


@router.message(form.interest)
async def interest_from_user(message: Message, state:FSMContext):
    interest_sex = ['Парни', 'Девушки', 'Все равно']
    if not (message.text in interest_sex):
        await message.answer('Такого варианта нет...')
    else:
        user_id = message.from_user.id
        index = interest_sex.index(message.text)
        await state.update_data(interest=index)
        await message.answer('Теперь нужно узнать откуда ты', reply_markup=kb.location(user_id))
        await state.set_state(form.location)


@router.message(F.content_type == 'location', form.location)
async def location_from_user(message: Message, state:FSMContext):
    user_id = message.from_user.id
    user_latitude = float(message.location.latitude)
    user_longitude = float(message.location.longitude)
    location_list = get_location_details(user_latitude, user_longitude)
    await state.update_data(location=location_list)
    await message.answer('Теперь пришлите ваше фото', reply_markup=kb.photo(user_id))
    await state.set_state(form.photo)


@router.message(form.location)
async def location_from_user(message: Message, state:FSMContext):
    user_id = message.from_user.id
    city = message.text
    location_list = get_city_details(city)
    if len(location_list):
        await state.update_data(location=location_list)
        await state.set_state(form.photo)
        await message.answer('Теперь пришлите ваше фото', reply_markup=kb.photo(user_id))
        await state.set_state(form.photo)
    else:
        await message.answer('Не знаю такого места...\n Попробуй написать его заного, вдруг ты допустил ошибку в написании')



@router.message(F.text == 'Взять из телеграмма', form.photo)
async def photo_from_tg(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo = await take_user_photo_tg(bot, user_id)
    await state.update_data(photo=photo)
    await message.answer('Напиши что-нибудь о себе.\nЕсли не хочешь ничего писать,то нажми кнопку "Пропустить"',
                         reply_markup=kb.description(user_id))
    await state.set_state(form.description)

#FIXXXXXXXXX
@router.message(F.text == 'Взять текущее фото', form.photo)
async def photo_from_tg(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo = get_photo(user_id)
    #await state.update_data(photo=photo)
    await message.answer('Напиши что-нибудь о себе.\nЕсли не хочешь ничего писать,то нажми кнопку "Пропустить"',
                         reply_markup=kb.description(user_id))
    await state.set_state(form.description)

@router.message(F.photo, form.photo)
async def photo_from_user(message: Message, state:FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    photo = await bot.download_file(file_path)
    await state.update_data(photo=photo)
    await message.answer('Напиши что-нибудь о себе.\nЕсли не хочешь ничего писать,то нажми кнопку "Пропустить"',
                         reply_markup=kb.description(user_id))
    await state.set_state(form.description)



@router.message(form.description)
async def description_from_user(message: Message, state:FSMContext):
    user_id = message.from_user.id
    description = message.text
    flag = True
    if (description == 'Пропустить'):
        await state.set_state(form.finish)
    elif (description == 'Оставить текущее'):
        current_description = get_description(user_id)
        if current_description != None:
            await state.update_data(desciption=current_description)
    else:
        if len(str(description)) > 964:
            difference = abs(len(str(description)) - 964)
            await message.answer(f'Количество символов превышено на ***{difference}***.\n'
                                 f'Попробуйте сделать текст менее объёмным', parse_mode='markdown')
            flag = False
        else:
            await state.update_data(description=description)
    if flag:
        await state.set_state(form.finish)
        await message.answer('Подтвердите создание анкеты', reply_markup=kb.confirm)

@router.message(form.finish)
async def finish_form(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    username = user.username
    await id_to_db(user_id)
    data = await state.get_data()
    data_name = data.get('name')
    data_sex = data.get('sex')
    data_age = data.get('age')
    data_interest = data.get('interest')
    data_description = data.get('description')
    data_photo = data.get('photo')
    data_location = data.get('location')
    await all_info_to_db(user_id, data_name, username, data_photo, data_age,
                         data_sex, data_description, data_interest)
    await location_to_db(user_id,data_location[0], data_location[1], data_location[2], data_location[3])
    await message.answer('Ваша анкета создана!!!', reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)
    await update_active(user_id, 1)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("edit"))
async def edit_form(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    user_id = user.id
    data = (callback_query.data.split("_")[1])
    if data == 'form':
        await callback_query.message.edit_reply_markup(reply_markup=kb.form_setting())
    if data == 'all':
        await callback_query.message.delete()
        await callback_query.message.answer('Введите ваше имя', reply_markup=kb.from_tg)
        await state.set_state(form.name)
    elif data == 'name':
        await callback_query.message.delete()
        await callback_query.message.answer('Введите ваше имя', reply_markup=kb.from_tg)
        await state.set_state(update.name)
    elif data == 'age':
        await callback_query.message.delete()
        await callback_query.message.answer('Введите ваш возраст', reply_markup=kb.age(user_id))
        await state.set_state(update.age)
    elif data == 'sex':
        await callback_query.message.delete()
        await callback_query.message.answer('Выберите ваш пол', reply_markup=kb.sex)
        await state.set_state(update.sex)
    elif data == 'desc':
        await callback_query.message.delete()
        await callback_query.message.answer('Расскажите о себе', reply_markup=kb.description(user_id))
        await state.set_state(update.description)
    elif data == 'location':
        await callback_query.message.delete()
        await callback_query.message.answer('Расскажи откуда ты', reply_markup=kb.location(user_id))
        await state.set_state(update.location)
    elif data == 'photo':
        await callback_query.message.delete()
        await callback_query.message.answer('Присылай новую фотографию', reply_markup=kb.photo(user_id))
        await state.set_state(update.photo)
    elif data == 'search':
        await callback_query.message.edit_reply_markup(reply_markup=kb.form_search_detail())
    elif data == 'active':
        await callback_query.message.edit_reply_markup(reply_markup=kb.form_active(user_id))
    elif data == 'on':
        await callback_query.message.delete()
        await update_active(user_id, 1)
        await callback_query.message.answer('Теперь ваша анкета активна!')
        await send_form_to_user(bot, user_id)
    elif data == 'off':
        await callback_query.message.delete()
        await update_active(user_id, 0)
        await callback_query.message.answer('Теперь ваша анкета не активна!')
        await send_form_to_user(bot, user_id)


@router.message(update.name)
async def edit_name(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    if (message.text == 'Взять из телеграмма'):
        name = user.first_name
        await update_name(user_id, name)
    else:
        name = message.text
        await update_name(user_id, name)
    await state.clear()
    await message.answer('Имя успешно обновлено', reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)


@router.message(update.age)
async def edit_age(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    age = message.text
    try:
        age = int(age)
        if age >= 13:
            await update_age(user_id, age)
            await state.clear()
            await message.answer('Возраст успешно обновлен', reply_markup=ReplyKeyboardRemove())
            await send_form_to_user(bot, user_id)
        else:
            await message.answer('Извините, ботом можно пользоваться, только, если вам больше 12')
    except ValueError:
        await message.answer('Это не возраст!!!')


@router.message(update.sex)
async def edit_sex(message: Message, state:FSMContext):
    user_id = message.from_user.id
    sex = ['Парень', 'Девушка']
    if not(message.text in sex):
        await message.answer('Такого варианта нет...')
    else:
        index = sex.index(message.text)
        await update_sex(user_id, index)
        await state.clear()
        await message.answer('Ваш пол обновлен', reply_markup=ReplyKeyboardRemove())
        await send_form_to_user(bot, user_id)


@router.message(update.description)
async def edit_description(message: Message, state:FSMContext):
    user_id = message.from_user.id
    description = message.text
    if (description == 'Пропустить'):
        await state.clear()
        await update_description(user_id, "")
        await message.answer('Описание профиля успешно обновлено',  reply_markup=ReplyKeyboardRemove())
        await send_form_to_user(bot, user_id)
    elif (description == 'Оставить текущее'):
        current_description = get_description(user_id)
        if current_description != None:
            await message.answer('Описание профиля осталось без изменений', reply_markup=ReplyKeyboardRemove())
            await send_form_to_user(bot, user_id)
    else:
        if len(str(description)) > 964:
            difference = abs(len(str(description)) - 964)
            await message.answer(f'Количество символов превышено на ***{difference}***.\n'
                                 f'Попробуйте сделать текст менее объёмным', parse_mode='markdown')
        else:
            await state.clear()
            await update_description(user_id, description)
            await message.answer('Описание профиля успешно обновлено', reply_markup=ReplyKeyboardRemove())
            await send_form_to_user(bot, user_id)


@router.message(F.content_type == 'location', update.location)
async def update_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_latitude = float(message.location.latitude)
    user_longitude = float(message.location.longitude)
    location_list = get_location_details(user_latitude, user_longitude)
    await location_to_db(user_id, location_list[0], location_list[1], location_list[2], location_list[3])
    await state.clear()
    await message.answer('Данные о местоположении обновлены!',reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)


@router.message(update.location)
async def update_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text
    location_list = get_city_details(city)
    if len(location_list):
        await location_to_db(user_id, location_list[0], location_list[1], location_list[2], location_list[3])
        await state.clear()
        await message.answer('Данные о местоположении обновлены!', reply_markup=ReplyKeyboardRemove())
        await send_form_to_user(bot, user_id)
    else:
        await message.answer('Не знаю такого места...\n Попробуй написать его заново, вдруг ты допустил ошибку в написании')


@router.message(F.text == 'Взять из телеграмма', update.photo)
async def update_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo = await take_user_photo_tg(bot, user_id)
    await photo_to_db(user_id, photo)
    await message.answer('Теперь фотография в анкете, как на твоей аватарке',
                         reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)
    await state.clear()

@router.message(F.text == 'Взять текущее фото', update.photo)
async def update_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer('Хорошо, оставляем текущую фотографию',
                         reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)
    await state.clear()

@router.message(F.photo, update.photo)
async def update_photo(message: Message, state:FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    photo = await bot.download_file(file_path)
    await photo_to_db(user_id, photo)
    await message.answer('Фотография успешно обновлена!',
                         reply_markup=ReplyKeyboardRemove())
    await send_form_to_user(bot, user_id)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("search"))
async def edit_search(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    user_id = user.id
    data = (callback_query.data.split('_')[1])
    location_list = ['Искать в моем городе', 'Искать в моей области', 'Искать моем округе', 'Искать моей стране']
    if data == 'sex':
        await callback_query.message.delete()
        await callback_query.message.answer('Кто тебе интересен?', reply_markup=kb.interest)
        await state.set_state(update.interest)
    elif data == 'location':
        await callback_query.message.delete()
        index = await get_search_priority(user_id)
        await callback_query.message.answer(f'Сейчас установлен режим\n***{location_list[index]}***',
                                            reply_markup=kb.form_search_location(), parse_mode='markdown')
    elif data == 'city':
        index = 0
        await update_search_priority(user_id, index)
        await callback_query.message.edit_text(f'Сейчас установлен режим\n***{location_list[index]}***'
                                            ,parse_mode='markdown', reply_markup=kb.form_search_location())
    elif data == 'state':
        index = 1
        await update_search_priority(user_id, index)
        await callback_query.message.edit_text(f'Сейчас установлен режим\n***{location_list[index]}***'
                                               , parse_mode='markdown', reply_markup=kb.form_search_location())
    elif data == 'region':
        index = 2
        await update_search_priority(user_id, index)
        await callback_query.message.edit_text(f'Сейчас установлен режим\n***{location_list[index]}***'
                                               , parse_mode='markdown', reply_markup=kb.form_search_location())
    elif data == 'country':
        index = 3
        await update_search_priority(user_id, index)
        await callback_query.message.edit_text(f'Сейчас установлен режим\n***{location_list[index]}***'
                                               , parse_mode='markdown', reply_markup=kb.form_search_location())

@router.message(update.interest)
async def update_interest_(message: Message, state:FSMContext):
    interest_sex = ['Парни', 'Девушки', 'Все равно']
    if not (message.text in interest_sex):
        await message.answer('Такого варианта нет...')
    else:
        user_id = message.from_user.id
        index = interest_sex.index(message.text)
        await update_interest(user_id, index)
        await message.answer('Хорошо, учтем твои интересы', reply_markup=ReplyKeyboardRemove())
        await send_form_to_user(bot, user_id)
        await state.clear()



@router.callback_query(lambda c: c.data.startswith("back"))
async def back(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    user_id = user.id
    data = (callback_query.data.split("_")[1])
    if data == 'menu':
        await callback_query.message.edit_reply_markup(reply_markup=kb.form_menu())
        await callback_query.message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)
    elif data == 'search':
        await callback_query.message.delete()
        await send_form_to_user(bot, user_id, kb.form_search_detail())
        await callback_query.message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)


