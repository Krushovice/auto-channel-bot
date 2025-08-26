import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from core.config import settings
from core.schemas import Application
from utils.notifications import notify_email


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("test"))
async def test_email(message: Message):
    # Разрешаем только администраторам
    if message.from_user.id != settings.bot.admin_id:
        return await message.answer("Недостаточно прав.")

    dummy = Application(
        tg_user_id=message.from_user.id,
        name="Тест",
        city="Тестоград",
        car="Toyota Prius",
        budget="1.2–1.5 млн",
        year="2017+",
        mileage="до 80 000",
        extras="Камеры, адаптивный круиз",
        contact="@your_contact",
    )

    await notify_email(dummy)
    await message.answer("Пробная отправка email инициирована (смотри логи).")
