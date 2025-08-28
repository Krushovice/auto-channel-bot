import asyncio

from app_builder import build_bot_dispatcher
from utils.logger import setup_logging


async def main():
    setup_logging()
    bot, dp = build_bot_dispatcher()
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    asyncio.run(main())
