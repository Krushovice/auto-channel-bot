import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


# ========== NESTED CONFIGS ==========
class LoggingConfig(BaseModel):
    app_name: str
    log_dir: str

    log_level: LogLevel = "INFO"
    console_level: LogLevel = "INFO"
    file_level: LogLevel = "INFO"
    aiogram_level: LogLevel = "INFO"
    smtp_level: LogLevel = "INFO"

    @field_validator("log_dir", mode="after")
    @classmethod
    def _abs_dir(cls, v: str) -> str:
        return os.path.abspath(v)

    @property
    def info_log_path(self) -> str:
        return os.path.join(self.log_dir, f"{self.app_name}.info.log")

    @property
    def error_log_path(self) -> str:
        return os.path.join(self.log_dir, f"{self.app_name}.error.log")


class TelegramConfig(BaseModel):
    token: str
    admin_id: int


class StoreConfig(BaseModel):
    channel: str
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


class InfoConfig(BaseModel):
    proxy: str
    logistic: str
    body_repair: str
    detailing: str
    auction_stat: str
    auc_list: str


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
    info: InfoConfig
    logger: LoggingConfig


settings = Settings()
