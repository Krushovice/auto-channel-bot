from typing import Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        self._pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict,
    ):
        async with self._pool() as session:
            data["db_session"] = session
            return await handler(event, data)