import App.user_keyboards as kb
from BotData.database_function import *
from App.states import *
from .function import *

from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from BotData.config import bot_token

bot = Bot(token=bot_token)
router_search = Router()

@router_search.message(F.text == 'Начать поиск')
async def in_search(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(Search.in_search)
    user = message.from_user
    user_id = user.id
    data = await state.get_data()
    count_skip = data.get('count_skip')
    flag = False
    if count_skip == None:
        await state.update_data(count_skip=0)
        flag = True
    if flag:
        data = await state.get_data()
        count_skip = data.get('count_skip')

    list_partner = await get_partner(user_id, 10, count_skip)
    if len(list_partner):
        await send_partner_form_to_user(bot, user_id, list_partner[0], kb.scroll)
        await state.update_data(last_id_search=list_partner[0])
    else:
        await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                                            reply_markup=kb.form_search_detail())



@router_search.message(Search.in_search)
async def in_search(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_text = message.text
    if user_text == '❤️':
        data = await state.get_data()
        count_skip = int(data.get('count_skip')) + 1
        last_id = data.get('last_id_search')
        await like_to_db(user_id, last_id)
        await send_like(bot, last_id)
        await message.answer('Пользователю отправлена ваша симпатия')

        await state.update_data(count_skip=count_skip)
        list_partner = await get_partner(user_id, 10, count_skip)
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('count_skip')) + 1
            await state.update_data(count_skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[index], kb.scroll)
            await state.update_data(last_id_search=list_partner[index])
        else:
            await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                                 reply_markup=kb.form_search_detail())
    elif user_text == '❌':
        data = await state.get_data()
        count_skip = int(data.get('count_skip')) + 1
        await state.update_data(count_skip=count_skip)
        last_id = data.get('last_id_search')
        list_partner = await get_partner(user_id, 10, count_skip)
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('count_skip')) + 1
            await state.update_data(count_skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[index], kb.scroll)
            await state.update_data(last_id_search=list_partner[index])
        else:
            await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                                 reply_markup=kb.form_search_detail())
    elif user_text == '💌':
        await state.set_state(Search.send_message)
        await message.answer('Пишите сообщение', reply_markup=kb.undo)

    elif user_text == 'Выйти из поиска':
        await state.clear()
        await message.answer('Поиск завершен, ждем вас еще!')
        await send_form_to_user(bot, user_id)
        await message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)

    elif user_text == 'Отправить жалобу':
        await state.set_state(Search.report)
        await message.answer('Напишите жалобу', reply_markup=kb.undo)





@router_search.message(Search.send_message)
async def send_message(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_text = message.text
    if user_text != 'Отменить':
        data = await state.get_data()
        count_skip = int(data.get('count_skip')) + 1
        last_id = data.get('last_id_search')
        await like_to_db(user_id, last_id, user_text)
        await send_like(bot, last_id)
        await message.answer('Пользователю отправлена ваша симпатия и сообщение')

        list_partner = await get_partner(user_id, 10, count_skip)
        last_id = data.get('last_id_search')
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('count_skip')) + 1
            await state.update_data(count_skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[index], kb.scroll)
            await state.update_data(last_id_search=list_partner[index])
        else:
            await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                                 reply_markup=kb.form_search_detail())
        await state.set_state(Search.in_search)
    else:
        await message.answer('Хорошо, не отправляем сообщение!')
        data = await state.get_data()
        count_skip = int(data.get('count_skip')) + 1
        await state.update_data(count_skip=count_skip)
        list_partner = await get_partner(user_id, 10, count_skip)
        last_id = data.get('last_id_search')
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('count_skip')) + 1
            await state.update_data(count_skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[index], kb.scroll)
            await state.update_data(last_id_search=list_partner[index])
        else:
            await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                                 reply_markup=kb.form_search_detail())

@router_search.message(Search.report)
async def send_message(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_message = message.text
    data = await state.get_data()
    count_skip = int(data.get('count_skip')) + 1
    await state.update_data(count_skip=count_skip)
    last_id = data.get('last_id_search')
    list_partner = await get_partner(user_id, 10, count_skip)
    await send_report(last_id, user_message)
    await message.answer('Жалоба успешно отправлена! Переходим к другому человеку')
    index = 0
    if (len(list_partner) and list_partner[index] == last_id):
        count_skip = int(data.get('count_skip')) + 1
        await state.update_data(count_skip=count_skip)
        index += 1
    if len(list_partner) > index:
        await send_partner_form_to_user(bot, user_id, list_partner[index], kb.scroll)
        await state.update_data(last_id_search=list_partner[index])
    else:
        await message.answer('К сожалению, подходящих партнеров нет, попробуйте расширить поиск(',
                             reply_markup=kb.form_search_detail())
    await state.set_state(Search.in_search)


@router_search.callback_query(lambda c: c.data.startswith("shows_more"))
async def shows_more(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user = callback_query.from_user
    user_id = user.id
    data = await state.get_data()
    count_skip = data.get('skip')
    await state.set_state(View_likes.in_view)
    flag = False
    if count_skip == None:
        await state.update_data(skip=0)
        flag = True
    if flag:
        data = await state.get_data()
        count_skip = data.get('skip')

    list_partner = await like_list(user_id, 10, count_skip)
    last_id = data.get('last_id_view')
    index = 0
    if (len(list_partner)):
        count_skip = int(data.get('skip')) + 1
        await state.update_data(skip=count_skip)
        index += 1
    if len(list_partner) > index:
        await send_partner_form_to_user(bot, user_id, list_partner[0], kb.view_like, True)
        await state.update_data(last_id_view=list_partner[index])
    else:
        await callback_query.message.answer('К сожалению, симпатии закончились(\n Но обязательно будут еще!')
        await state.clear()
        await send_form_to_user(bot, user_id)
        await callback_query.message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)


@router_search.message(View_likes.in_view)
async def view_like(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_text = message.text
    if user_text == '❤️':
        data = await state.get_data()
        count_skip = data.get('skip')
        list_partner = await like_list(user_id, 10, count_skip)
        partner = list_partner[0]
        username_partner = get_username(partner)
        username_user = get_username(user_id)
        await message.answer(f'У вас с @{username_partner} взаимная симпатия')
        await send_username_to_partner(bot, partner, user_id, username_user)
        count_skip = int(data.get('skip')) + 1
        await state.update_data(skip=count_skip)
        list_partner = await like_list(user_id, 10, count_skip)
        last_id = data.get('last_id_view')
        await del_like(last_id, user_id)
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('skip')) + 1
            await state.update_data(skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[0], kb.view_like, True)
            await state.update_data(last_id_view=list_partner[index])
        else:
            await message.answer('К сожалению, симпатии закончились(\n Но обязательно будут еще!')
            await state.clear()
            await send_form_to_user(bot, user_id)
            await message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)
    elif user_text == '❌':
        data = await state.get_data()
        count_skip = int(data.get('skip')) + 1
        last_id = data.get('last_id_view')
        await state.update_data(skip=count_skip)
        list_partner = await like_list(user_id, 10, count_skip)
        await del_like(last_id, user_id)
        index = 0
        if (len(list_partner) and list_partner[index] == last_id):
            count_skip = int(data.get('skip')) + 1
            await state.update_data(skip=count_skip)
            index += 1
        if len(list_partner) > index:
            await send_partner_form_to_user(bot, user_id, list_partner[0], kb.view_like, True)
            await state.update_data(last_id_view=list_partner[index])
        else:
            await message.answer('К сожалению, симпатии закончились(\n Но обязательно будут еще!')
            await state.clear()
            await send_form_to_user(bot, user_id)
            await message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)
    elif user_text == 'Выйти из просмотра':
        await send_like(bot, user_id)
        await state.clear()
        await send_form_to_user(bot, user_id)
        await message.answer('Чтобы продолжить поиск нажми кнопку', reply_markup=kb.start_search)