import logging

from aiogram import Router, F
from aiogram.types import Message

from core.config import settings
from markups.main_kb import WELCOME_KB

from utils.texts import WELCOME

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        text=WELCOME.format(channel=settings.store.channel),
        reply_markup=WELCOME_KB,
    )
