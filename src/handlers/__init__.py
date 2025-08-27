__all__ = ("router",)

from aiogram import Router

from .commands.main_commands import router as commands_router
from .callback_handlers.order_form_handlers import router as order_callbacks_router
from .callback_handlers.main_cb_handlers import router as main_callbacks_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    order_callbacks_router,
    main_callbacks_router,
)
