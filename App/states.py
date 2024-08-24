from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

class form(StatesGroup):
    name = State()
    sex = State()
    age = State()
    interest = State()
    description = State()
    location = State()
    photo = State()
    finish = State()

class update(StatesGroup):
    name = State()
    sex = State()
    age = State()
    interest = State()
    description = State()
    location = State()
    photo = State()

class Search(StatesGroup):
    in_search = State()
    send_message = State()
    current_index = State()
    count_skip = State()
    last_id_search = State()
    report = State()

class View_likes(StatesGroup):
    in_view = State()
    skip = State()
    last_id_view = State()


class Admin(StatesGroup):
    authorized = State()
    message = State()
    mailing = State()
    view_report = State()