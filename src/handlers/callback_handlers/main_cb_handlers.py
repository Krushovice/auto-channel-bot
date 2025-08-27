import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from core.config import settings
from handlers.commands.main_commands import cmd_start
from markups.main_kb import BACK_KB
from utils.texts import USEFUL_INFO_TEMPLATE

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "links")
async def handle_links_button(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer(
        USEFUL_INFO_TEMPLATE.format(
            YOUTUBE=settings.store.youtube,
            AUC_STAT=settings.info.auction_stat,
            DETAILING=settings.info.detailing,
            PROXY=settings.info.proxy,
            BODY_REPAIR=settings.info.body_repair,
            LOGISTIC=settings.info.logistic,
            AUC_LIST=settings.info.auc_list,
        ),
        reply_markup=BACK_KB,
    )


@router.callback_query(F.data == "back")
async def handle_back_button(cb: CallbackQuery):
    await cb.answer()
    await cmd_start(message=cb.message)
