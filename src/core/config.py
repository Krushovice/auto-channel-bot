from pathlib import Path

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


# ========== NESTED CONFIGS ==========
class TelegramConfig(BaseModel):
    token: str
    admin_id: int


class StoreConfig(BaseModel):
    channel_link: str
    youtube: str
    chat: str
    site: str
    manager_tg: str


class EmailConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_password: str
    smtp_user: str
    send_from: EmailStr
    send_to: EmailStr


# ========== ROOT SETTINGS ==========
class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(str(BASE_DIR / ".env"),),
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file_encoding="utf-8",
        validate_default=False,
    )

    bot: TelegramConfig
    store: StoreConfig
    email: EmailConfig


settings = Settings()
