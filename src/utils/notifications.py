import logging
from email.message import EmailMessage

import aiosmtplib
from aiogram import Bot


from core.config import settings
from core.schemas import Application


logger = logging.getLogger(__name__)


async def notify_admin(
    bot: Bot,
    text_html: str,
) -> None:
    try:
        await bot.send_message(
            settings.bot.admin_id,
            text_html,
            disable_web_page_preview=True,
        )
    except Exception:
        logger.exception(
            "Не удалось отправить заявку админу %s",
            settings.bot.admin_id,
        )


async def notify_email(app: Application) -> None:

    required = [
        settings.email.smtp_host,
        settings.email.smtp_port,
        settings.email.smtp_user,
        settings.email.smtp_password,
        settings.email.send_from,
        settings.email.send_to,
    ]
    if any(v in (None, [], "") for v in required):
        logger.error("Email включён, но не заданы SMTP/EMAIL настройки")
        return

    subject = "Новая заявка: автоподбор из Японии"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email.send_from
    msg["To"] = settings.email.send_to

    # Простой текст и HTML-версия
    plain = (
        f"Клиент TG ID: {app.tg_user_id}\n"
        f"Имя: {app.name}\nГород: {app.city}\nЗапрос: {app.car}\n"
        f"Бюджет: {app.budget}\nГод: {app.year}\nПробег: {app.mileage}\n"
        f"Опции: {app.extras}\nКонтакт: {app.contact}\n"
    )
    html = (
        "<h3>Новая заявка на автоподбор</h3>"
        f"<p><b>TG ID:</b> {app.tg_user_id}</p>"
        f"<p><b>Имя:</b> {app.name}</p>"
        f"<p><b>Город:</b> {app.city}</p>"
        f"<p><b>Запрос:</b> {app.car}</p>"
        f"<p><b>Бюджет:</b> {app.budget}</p>"
        f"<p><b>Год:</b> {app.year}</p>"
        f"<p><b>Пробег:</b> {app.mileage}</p>"
        f"<p><b>Опции:</b> {app.extras}</p>"
        f"<p><b>Контакт:</b> {app.contact}</p>"
    )

    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.email.smtp_host,
            port=settings.email.smtp_port,
            username=settings.email.smtp_user,
            password=settings.email.smtp_password,
            start_tls=True,
        )
    except Exception:
        logger.exception("Не удалось отправить письмо с заявкой")


async def notify_all(
    bot: Bot,
    app: Application,
    full_name: str,
) -> None:
    html = app.to_summary(full_name)
    await notify_admin(bot, html)
    await notify_email(app)
