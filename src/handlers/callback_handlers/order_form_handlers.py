import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery


from utils.texts import ASKS, CONFIRM_TO_CLIENT, CANCELLED
from markups.main_kb import CANCEL_KB, REMOVE_KB
from core.schemas import Application
from utils.notifications import notify_all

from utils.fsm_data import ApplicationForm

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "apply:start")
async def apply_start(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ApplicationForm.name)
    await cb.message.answer(ASKS["name"], reply_markup=CANCEL_KB)
    await cb.answer()


@router.message(F.text == "❌ Отмена")
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCELLED, reply_markup=REMOVE_KB)


@router.message(ApplicationForm.name)
async def step_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(ApplicationForm.city)
    await message.answer(ASKS["city"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.city)
async def step_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.strip())
    await state.set_state(ApplicationForm.car)
    await message.answer(ASKS["car"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.car)
async def step_car(message: Message, state: FSMContext):
    await state.update_data(car=message.text.strip())
    await state.set_state(ApplicationForm.budget)
    await message.answer(ASKS["budget"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.budget)
async def step_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text.strip())
    await state.set_state(ApplicationForm.year)
    await message.answer(ASKS["year"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.year)
async def step_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text.strip())
    await state.set_state(ApplicationForm.mileage)
    await message.answer(ASKS["mileage"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.mileage)
async def step_mileage(message: Message, state: FSMContext):
    await state.update_data(mileage=message.text.strip())
    await state.set_state(ApplicationForm.extras)
    await message.answer(ASKS["extras"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.extras)
async def step_extras(message: Message, state: FSMContext):
    await state.update_data(extras=message.text.strip())
    await state.set_state(ApplicationForm.contact)
    await message.answer(ASKS["contact"], reply_markup=CANCEL_KB)


@router.message(ApplicationForm.contact)
async def step_contact(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(contact=message.text.strip())
    data = await state.get_data()
    await state.clear()

    user = message.from_user
    full_name = (
        " ".join(filter(None, [user.first_name, user.last_name])) or "Пользователь"
    )

    app = Application(
        tg_user_id=user.id,
        name=data.get("name", ""),
        city=data.get("city", ""),
        car=data.get("car", ""),
        budget=data.get("budget", ""),
        year=data.get("year", ""),
        mileage=data.get("mileage", ""),
        extras=data.get("extras", ""),
        contact=data.get("contact", ""),
    )

    # Ответ клиенту
    await message.answer(
        CONFIRM_TO_CLIENT,
        reply_markup=REMOVE_KB,
    )

    # 1) Уведомления (Telegram + Email)
    # Уведомления — в фоне
    task = asyncio.create_task(notify_all(bot, app, full_name))
    task.add_done_callback(
        lambda t: (
            logger.exception(
                "Notify task crashed",
                exc_info=t.exception(),
            )
            if t.exception()
            else None
        )
    )
