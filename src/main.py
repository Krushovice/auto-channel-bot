import asyncio

from build import build_bot_dispatcher


async def main():
    bot, dp = await build_bot_dispatcher()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),)


if __name__ == "__main__":
    asyncio.run(main())

