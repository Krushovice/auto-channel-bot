__all__ = ("router",)

from aiogram import Router

from .commands.main_commands import router as commands_router
from .callback_handlers.order_form_handlers import router as callbacks_router

router = Router(name=__name__)

router.include_routers(commands_router, callbacks_router)
