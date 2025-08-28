import re
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

_scheduler: Optional[AsyncIOScheduler] = None


def _normalize_channel(raw: str) -> str:
    """
    Принимает:
      - '@my_channel'
      - 'https://t.me/my_channel' / 't.me/my_channel'
      - '-1001234567890'
    Возвращает то, что можно напрямую передать в bot.send_message(...).
    """
    raw = raw.strip()
    if raw.startswith("-100") or raw.startswith("@"):
        return raw
    m = re.search(r"(?:t\.me/|https?://t\.me/)([A-Za-z0-9_]+)$", raw)
    if m:
        return f"@{m.group(1)}"
    # на крайний случай — пусть будет как есть
    return raw


def _build_promo_text(bot_username: str) -> str:
    # HTML разметка (parse_mode=HTML)
    return (
        "<b>🇯🇵 Авто из Японии — заявки в 1 клик</b>\n"
        "Оставьте параметры — подберём варианты с аукционов, расчётом «до ключей» и отчётами.\n\n"
        f'👉 <a href="https://t.me/{bot_username}">Открыть бота</a>\n'
    )


async def _send_promo(bot: Bot, channel: str) -> None:
    me = await bot.get_me()
    username = me.username or ""  # на всякий случай
    text = _build_promo_text(username)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оставить заявку в боте",
                    url=f"https://t.me/{username}",
                )
            ]
        ]
    )

    await bot.send_message(
        chat_id=_normalize_channel(channel),
        text=text,
        reply_markup=kb,
        disable_web_page_preview=True,
    )


def setup_promo_scheduler(
    bot: Bot,
    channel: str,
    *,
    run_now: bool = True,
) -> None:
    """
    Стартует планировщик, который шлёт промо в канал каждые 3 дня.
    """
    global _scheduler
    if _scheduler and _scheduler.running:
        return

    _scheduler = AsyncIOScheduler(timezone=None)  # без TZ, интервал от тикинга цикла
    # первый запуск — сразу (или через 3 дня, если run_now=False)
    next_time = datetime.now() if run_now else datetime.now() + timedelta(days=3)

    _scheduler.add_job(
        _send_promo,
        trigger="interval",
        days=10,
        args=[bot, channel],
        id="promo_every_10_days",
        replace_existing=True,
        next_run_time=next_time,
        coalesce=True,  # слить пропуски, если процесс не работал
        max_instances=1,  # не параллелить
        misfire_grace_time=3600,  # час на отставание
    )
    _scheduler.start()


async def stop_promo_scheduler() -> None:
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
    _scheduler = None
