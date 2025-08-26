from pydantic import BaseModel, Field
from datetime import datetime


class Application(BaseModel):
    tg_user_id: int
    name: str
    city: str
    car: str
    budget: str
    year: str
    mileage: str
    extras: str
    contact: str
    created_at: datetime = Field(default_factory=datetime.now)

    def to_summary(self, full_name: str) -> str:
        return (
            "📝 <b>Новая заявка на подбор авто</b>\n\n"
            f'👤 Клиент: <a href="tg://user?id={self.tg_user_id}">{full_name}</a> '
            f"(id: <code>{self.tg_user_id}</code>)\n"
            f"📍 Город: <b>{self.city}</b>\n"
            f"🚘 Запрос: <b>{self.car}</b>\n"
            f"💰 Бюджет: <b>{self.budget}</b>\n"
            f"📅 Год: <b>{self.year}</b>\n"
            f"📏 Пробег: <b>{self.mileage}</b>\n"
            f"✨ Опции: <b>{self.extras}</b>\n"
            f"☎️ Контакт: <b>{self.contact}</b>\n"
        )
