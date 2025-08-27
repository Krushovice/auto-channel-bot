from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from core.config import settings

CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]], resize_keyboard=True
)

WELCOME_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚗 Оставить заявку",
                callback_data="apply:start",
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Наш Чат",
                url=settings.store.chat,
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 Написать менеджеру",
                url=settings.store.manager_tg,
            )
        ],
        [
            InlineKeyboardButton(
                text="📎 Полезные ссылки",
                callback_data="links",
            )
        ],
    ]
)
BACK_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Вернуться",
                callback_data="back",
            )
        ]
    ]
)
REMOVE_KB = ReplyKeyboardRemove()
