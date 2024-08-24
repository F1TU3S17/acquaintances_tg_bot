import App.user_keyboards as kb
from BotData.database_function import *
from App.states import *
from App.function import *

from aiogram import Router, Bot, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from BotData.config import bot_token, admin_id
import App.admin_keyboards as ad_kb


bot = Bot(token=bot_token)
router_admin = Router()

@router_admin.message(Command('admin'))
async def admin(message:Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    admin_in_db = await check_admin(user_id)
    if user_id == admin_id or admin_in_db:
        await message.answer('Вы действительно администратор!',reply_markup=ad_kb.admin)
        await state.set_state(Admin.authorized)
    else:
        await message.answer('Вы не являетесь администратором')


@router_admin.message(F.text == 'Создать рассылку', Admin.authorized)
async def start_mailing(message: Message, state: FSMContext):
    await message.answer('Хорошо, давайте создадим рассылку.\nДля этого отправьте сообщение, которое хотите разослать',
                         reply_markup=ad_kb.admin)
    await state.set_state(Admin.message)

@router_admin.message(Admin.message)
async def get_message_mailing(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Что дальше?', reply_markup=ad_kb.send)
    await state.set_state(Admin.mailing)

@router_admin.message(Admin.mailing)
async def go_mailing(message: Message, state: FSMContext):
    await state.update_data(mailing=message.text)
    data = await state.get_data()
    mailing = data.get('mailing')
    if mailing == 'Отправить':
        data_message = str(data.get('message'))
        users = await users_list()
        await message.answer('***Выполняем рассылку***⏳', parse_mode='Markdown')
        counter = 0
        for i in users:
            await bot.send_message(i, data_message)
            counter += 1
        await message.answer(f'***Сообщение доставлено всем*** ___"{counter}"___ ***пользователям***📧', parse_mode='Markdown', reply_markup=ad_kb.admin)
    else:
        await message.answer('Как вам угодно😊', reply_markup=ad_kb.admin)
    await state.clear()
    await state.set_state(Admin.authorized)



@router_admin.message(F.text =='Просмотр жалоб', Admin.authorized)
async def view_report(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    await state.set_state(Admin.view_report)
    report = await f_report()
    if len(report):
        await send_partner_form_to_user(bot, user_id, report[0], ReplyKeyboardRemove())
        await message.answer(f'❗️ТЕКСТ ЖАЛОБЫ К ДАННОЙ АНКЕТЕ❗️\n{report[1]}',reply_markup=ad_kb.report)
    else:
        await message.answer('Жалоб нет!', reply_markup=ad_kb.admin)
        await state.set_state(Admin.authorized)



@router_admin.message(Admin.view_report)
async def view_report(message: Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    user_text = message.text
    report = await f_report()
    flag = True
    if user_text == 'Заблокировать анкету':
        await del_form(report[0])
        await del_report(report[0], report[1], True)
        await bot.send_message(report[0],'Ваша анкета была заблокирована!\n '
                                         'Вы можете создать новую, для этого пропишите /start')
    elif user_text == 'Далее':
        await del_report(report[0], report[1])
    elif user_text == 'Выйти':
        await message.answer('Вы можете продолжить просмотр жалоб позднее', reply_markup=ad_kb.admin)
        await state.set_state(Admin.authorized)
    else:
        await message.answer('Такой команды не существует')
        flag = False
    if flag:
        report = await f_report()
        if len(report):
            await send_partner_form_to_user(bot, user_id, report[0], ReplyKeyboardRemove())
            await message.answer(f'❗️ТЕКСТ ЖАЛОБЫ К ДАННОЙ АНКЕТЕ❗️\n{report[1]}', reply_markup=ad_kb.report)
        else:
            await message.answer('Жалоб нет!',reply_markup=ad_kb.admin)
            await state.set_state(Admin.authorized)