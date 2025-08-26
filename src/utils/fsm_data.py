from aiogram.fsm.state import StatesGroup, State


class ApplicationForm(StatesGroup):
    name = State()
    city = State()
    car = State()
    budget = State()
    year = State()
    mileage = State()
    extras = State()
    contact = State()
