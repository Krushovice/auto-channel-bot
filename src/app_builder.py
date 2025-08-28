from typing import Tuple

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from handlers import router as main_router
from admin.routes import router as admin_router
from utils.promo_scheduler import setup_promo_scheduler, stop_promo_scheduler


def build_bot_dispatcher() -> Tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()

    # планировщик: старт/стоп
    @dp.startup.register
    async def _on_startup():
        setup_promo_scheduler(bot, settings.store.channel, run_now=True)

    @dp.shutdown.register
    async def _on_shutdown():
        await stop_promo_scheduler()

    dp.include_routers(main_router, admin_router)
    return bot, dp
