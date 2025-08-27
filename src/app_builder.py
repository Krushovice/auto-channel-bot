from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from handlers import router as main_router
from admin.routes import router as admin_router


async def build_bot_dispatcher() -> tuple[Bot, Dispatcher]:

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_routers(main_router, admin_router)

    return bot, dp
